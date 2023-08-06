import numpy as np
import pandas as pd
import attr
from attr.validators import instance_of
from enum import Enum, auto


class LineSignalType(Enum):
    """ All possible types of correct/incorrect line signals """

    VALID_UNIDIR = auto()
    VALID_BIDIR = auto()
    EXTRA_LINES = auto()
    SINGLE_PIXEL = auto()


@attr.s(slots=True)
class LineRectifier:
    """
    Receives the input lines and makes sure that they're OK and will render a good volume.

    Returns the np.array with the corrected lines.

    Errors - ``ValueError`` if signal can't be corrected.
    """

    lines = attr.ib(validator=instance_of(np.ndarray))  # raw line signal
    x_pixels = attr.ib(
        default=512, validator=instance_of(int)
    )  # number of expected lines
    bidir = attr.ib(default=False, validator=instance_of(bool))  # bidir or unidir scan
    ALLOWED_THRESHOLD = attr.ib(default=0.1, validator=instance_of(float))
    end_time = attr.ib(default=np.uint64(1), validator=instance_of(np.uint64))
    rectified_lines = attr.ib(init=False)  # returned signal
    __process_method = attr.ib(init=False)

    def rectify(self) -> np.ndarray:
        """ Main method to run the validation process on the line signal """
        signal_type = self.__assess_line_sig()
        self.rectified_lines = self.__process_method[signal_type]()
        return self.rectified_lines

    def __attrs_post_init__(self):
        """
        Generate a basic dictionary to choose the right processing method
        :return:
        """
        self.__process_method = {
            LineSignalType.EXTRA_LINES: self.__truncate_extra_lines,
            LineSignalType.VALID_UNIDIR: self.__preprocess_unidir_lines,
            LineSignalType.VALID_BIDIR: self.__preprocess_bidir_lines,
            LineSignalType.SINGLE_PIXEL: self.__single_pixel,
        }

    def __assess_line_sig(self) -> LineSignalType:
        """ Preliminary effort to detect the quality of the line signal """
        self.lines.sort()
        num_of_lines = len(self.lines)
        if num_of_lines > 1:
            if (
                np.abs(1 - (num_of_lines / self.x_pixels)) > self.ALLOWED_THRESHOLD
            ):  # line signal was too corrupt
                if (
                    num_of_lines >= self.x_pixels
                ):  # corrupt, but due to some extra lines
                    return LineSignalType.EXTRA_LINES
                else:  # really too corrupt
                    raise ValueError

            else:  # lines signal is corrupt, but we can save it
                return (
                    LineSignalType.VALID_BIDIR
                    if self.bidir
                    else LineSignalType.VALID_UNIDIR
                )

        else:  # single pixel frames, perhaps
            return LineSignalType.SINGLE_PIXEL

    def __truncate_extra_lines(self) -> np.ndarray:
        """ Called when the line signal is both dirty and contains extra lines """
        mean_diff = np.diff(self.lines).mean()
        return np.r_[
            self.lines[: self.x_pixels],
            np.array([self.lines[self.x_pixels - 1] + mean_diff], dtype=np.uint64),
        ]

    def __single_pixel(self) -> np.ndarray:
        """
        Dumbed down case of a single-pixel frame
        :return:
        """
        return np.linspace(
            self.lines[0], self.end_time, num=self.x_pixels + 1, endpoint=True
        )

    def __preprocess_unidir_lines(self) -> np.ndarray:
        """ Obtain the needed parameters for the rectify_lines method """
        lines = pd.Series(self.lines)
        diffs = lines.diff()
        rel_idx = np.where(
            np.abs(diffs.pct_change(periods=1)) > self.ALLOWED_THRESHOLD
        )[0]
        rel_diff = np.diff(rel_idx) == 2
        if rel_diff.shape[0] > 0 and sum(rel_diff) > 0:
            for idx in np.where(np.concatenate((rel_diff, np.array([False]))))[
                0
            ]:  # edge case
                rel_idx[idx + 1] -= 1
        mean_val = diffs.drop(rel_idx).mean()
        return self.__rectify_lines(
            lines=lines, diffs=diffs, mean_val=mean_val, rel_idx=rel_idx
        )

    def __preprocess_bidir_lines(self) -> np.ndarray:
        """ Obtain the needed parameters for the rectify_lines method """
        self.ALLOWED_THRESHOLD = 0.15  # x100 percent
        lines = pd.Series(self.lines)
        diff1 = lines.diff()
        diffs = lines.rolling(2).sum().diff()
        diffs[1] = diffs.mean()
        rel_idx = np.where(
            np.abs(diffs.pct_change(periods=1)) > self.ALLOWED_THRESHOLD
        )[0]
        if len(rel_idx) == 0:
            return self.__rectify_lines(
                lines=lines, diffs=diff1, mean_val=diff1.mean(), rel_idx=rel_idx
            )

        # if len(rel_idx) % 2 != 0:  # every misplaced line should have a start and an end
        #     raise ValueError
        idx_to_throw = np.array([], dtype=np.int64)
        if rel_idx.shape[0] > 1:
            for idx, _ in enumerate(rel_idx[::2]):
                try:
                    idx_to_throw = np.concatenate(
                        (
                            idx_to_throw,
                            np.arange(rel_idx[idx * 2], rel_idx[idx * 2 + 1] + 1),
                        )
                    )
                except IndexError:
                    idx_to_throw = np.concatenate((idx_to_throw, rel_idx[-1]))
        else:
            idx_to_throw = rel_idx.copy()

        final_rel_idx = rel_idx[::2]
        # Double jumps of rows missing
        rel_diff = np.diff(final_rel_idx) == 2
        if rel_diff.shape[0] > 0 and sum(rel_diff) > 0:
            for idx in np.where(np.concatenate((rel_diff, np.array([False]))))[
                0
            ]:  # edge case
                final_rel_idx[idx + 1] -= 1

        # Check for multiline double spacing
        double: np.ndarray = np.where(np.diff(rel_idx)[::2] == 4)[0]
        if len(double) > 0:
            for idx in double:
                indices_to_concat = [
                    place for place in range(rel_idx[idx] + 1, rel_idx[idx + 1])
                ]
                new_rel_idx = np.concatenate(
                    (
                        rel_idx[: idx + 1],
                        rel_idx[idx + 2 :],
                        np.array(indices_to_concat, dtype=np.int64),
                    )
                )
        else:
            new_rel_idx = sorted(rel_idx)[::2]
        final_rel_idx = np.unique(np.concatenate((final_rel_idx, new_rel_idx)))

        # Check for multiline triple spacing
        triple: np.ndarray = np.where(np.diff(rel_idx)[::2] == 5)[0]
        if len(triple) > 0:
            for idx in triple:
                indices_to_concat = [
                    place for place in range(rel_idx[idx] + 1, rel_idx[idx + 1])
                ]
                rel_idx = np.concatenate(
                    (rel_idx, np.array(indices_to_concat, dtype=np.int64))
                )
        else:
            rel_idx.sort()
        final_rel_idx = np.unique(np.concatenate((final_rel_idx, rel_idx)))

        mean_val = diff1.drop(idx_to_throw).mean()
        return self.__rectify_lines(
            lines=lines, diffs=diff1, mean_val=mean_val, rel_idx=final_rel_idx
        )

    def __rectify_lines(
        self, lines: pd.Series, diffs: pd.Series, mean_val: float, rel_idx: np.ndarray
    ) -> np.ndarray:
        """
        Rectify a semi-broken line signal.

        :return np.ndarray: Rectified lines
        """

        if rel_idx.shape[0] > 0.2 * self.x_pixels:  # too many missing lines
            raise ValueError

        if len(lines) - 1 in rel_idx:  # last lines are missing
            needed_lines = 1 + (self.x_pixels + 1 - (len(lines) + len(rel_idx)))
            if needed_lines < 1:
                raise ValueError
            lines = lines[:-1].append(
                pd.Series(
                    np.linspace(
                        start=lines.iloc[-2] + mean_val,
                        stop=lines.iloc[-2] + ((needed_lines + 1) * mean_val),
                        num=needed_lines,
                        dtype=np.uint64,
                    )
                )
            )
            rel_idx = rel_idx[rel_idx != len(diffs) - 1]
        if (
            np.abs((diffs.iloc[1] - mean_val) / mean_val) > self.ALLOWED_THRESHOLD
        ):  # first line came late
            rel_idx = np.r_[rel_idx, 1]
        if len(rel_idx) > 0:  # straight-forward addition of line signals
            for val in rel_idx:
                missing_lines = int(np.around(diffs[val] / mean_val)) - 1
                lines = lines.append(
                    pd.Series(
                        np.linspace(
                            start=lines.iloc[val - 1] + mean_val,
                            stop=lines.iloc[val],
                            endpoint=False,
                            num=missing_lines,
                            dtype=np.uint64,
                        )
                    )
                )

        if len(lines) != self.x_pixels:  # lines weren't recorded from the get-go
            if lines.iloc[0] == 0:  # we'll append at the end
                lines = lines.sort_values().reset_index(drop=True)
                needed_lines = np.abs(self.x_pixels - len(lines))
                lines = lines.append(
                    pd.Series(
                        np.linspace(
                            start=lines.iloc[-1] + mean_val,
                            stop=lines.iloc[-1] + (needed_lines + 1) * mean_val,
                            endpoint=False,
                            num=needed_lines,
                            dtype=np.uint64,
                        )
                    )
                )
            else:
                lines = lines.append(
                    pd.Series(
                        np.linspace(
                            start=0,
                            stop=lines.iloc[0],
                            endpoint=False,
                            num=np.abs(self.x_pixels - len(lines)),
                            dtype=np.uint64,
                        )
                    )
                )
        lines = lines.sort_values().reset_index(drop=True)
        lines = np.r_[
            lines.iloc[: self.x_pixels],
            np.array([lines.iloc[self.x_pixels - 1] + mean_val], dtype=np.uint64),
        ]
        return lines
