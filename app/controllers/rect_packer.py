import math
from copy import deepcopy

from rectpack import newPacker, skyline, PackingBin, pack_algo, SORT_SSIDE
from PIL import Image, ImageDraw

from config import BaseConfig as conf
from app.logger import log
from app.utils import generate_color_hex


class RectPacker:
    def __init__(
        self,
        blade_size: int = 0,
        is_sizes_equals: bool = False,
        square_unit: int = conf.METRIC_TO_SQR_UNIT_VALUE["cm"],
        price_per: str = "sqr",
        print_price: float = 0,
        moq: int = 1,
    ):
        """Init RectPacker instance with rectpack.racker object to
        find the optimal arrangement of rectangles on bin area and show it
        on image

        Args:
            blade_size (int, optional): Value that will be added
                to each side of rectangle. Defaults to 0.
            is_sizes_equals (bool, optional): Adds 1 to width to make it
                larger if sizes equals, to do correct calculations
        """
        self.is_sizes_equals = is_sizes_equals
        self.bins = []
        self.rectangles = []
        self.blade_size = blade_size
        self.bins_in_row = 1
        self.square_unit = square_unit
        self.price_per = price_per
        self.print_price = print_price
        self.moq = moq

        # data for reset
        self._bins = []
        self._rectangles = []

        self._result = {
            "not_placed_rectangles": [],
            "used_bins": self.bins_in_row,
            "bins": [],
        }

    @property
    def result(self):
        moq_price = self.print_price * self.moq

        used_bins_count = (
            self._result["used_bins"]
            if len(self._result["bins"]) == 1
            else len(self._result["bins"])
        )

        res = {
            "used_area": 0,
            "wasted_area": 0,
            "placed_items": [],
            "print_price": 0,
            "bins": [],
            "used_bins": used_bins_count,
        }
        for bin in self._result["bins"]:
            if self.is_sizes_equals:
                bin["sizes"][0] -= 1

            # wasted area calculated by max_y_coordinate * width
            reduced_height = bin["sizes"][1] - bin["max_y_coordinate"]
            if reduced_height <= 0:
                reduced_height = bin["sizes"][1]

            used_area = (bin["sizes"][0] * bin["max_y_coordinate"]) / self.square_unit
            wasted_area = bin["sizes"][0] * reduced_height / self.square_unit
            res["used_area"] += used_area
            if used_area != wasted_area:
                res["wasted_area"] += wasted_area
            else:
                res["wasted_area"] += 0
            res["placed_items"] += bin["rectangles"]

            if self.price_per == "sqr":
                res["print_price"] = res["used_area"] * self.print_price
            else:
                res["print_price"] = self.print_price * self.bins_in_row

            res["bins"].append(
                {
                    "sizes": bin["sizes"],
                    "used_area": bin["used_area"],
                    "wasted_area": bin["wasted_area"],
                    "placed_items": bin["rectangles"],
                    "print_price": (math.prod(bin["sizes"]) / self.square_unit)
                    * self.print_price,
                    "bin": bin["bin"],
                }
            )

        if res["print_price"] < moq_price and self.moq > 0:
            res["print_price"] = moq_price

        return res

    def reset(self, bins_in_row=1, reset_bin_sizes=False):
        """Remove all results"""
        self._result = {
            "not_placed_rectangles": [],
            "used_bins": bins_in_row,
            "bins": [],
        }
        self.bins_in_row = bins_in_row
        if reset_bin_sizes:
            self.bins = deepcopy(self._bins)

    def add_bin(self, width: int, height: int):
        """Add bin to bins list

        Args:
            width (int): bin width
            height (int): bin height
        """
        width += self.blade_size * 2
        height += self.blade_size * 2
        log(log.INFO, "Add bin [%s]", [width, height])
        self.bins.append([width, height])
        self._bins = deepcopy(self.bins)

    def add_rectangle(self, width: int, height: int):
        """Add rectangle to rectangles list

        Args:
            width (int): rectangle width
            height (int): rectangle height
        """
        log(log.INFO, "Add rectangle [%s]", [width, height])
        self.rectangles.append(sorted([width, height]))

    def validate_rectangles(self):
        """Check if addded rectangles is valid and can be placed on bin area

        Raises:
            ValueError: if bins are not added
            ValueError: if rectangles are not added
            ValueError: if found invalid rectangle
        """
        log(log.INFO, "Validate rectangles")

        if not self.bins:
            log(log.ERROR, "Bins not found")
            raise ValueError("Bins not found")
        elif not self.rectangles:
            log(log.ERROR, "Rectangles not found")
            raise ValueError("Rectangles not found")
        invalid_rectangles = []

        for rect in self.rectangles:
            rect = sorted(rect)
            fit_in_bins = []
            for bin in self.bins:
                bin = sorted(bin)
                fit_in_bins.append(
                    rect[0] + self.blade_size * 2 <= bin[0] + self.blade_size * 2
                    and rect[1] + self.blade_size * 2 <= bin[1] + self.blade_size * 2
                )
            if not all(fit_in_bins):
                invalid_rectangles.append(rect)

        if invalid_rectangles:
            log(log.ERROR, "Found invalid rectangle(s): [%s]", invalid_rectangles)

            raise ValueError(
                "Found invalid rectangle(s): %s"
                % ", ".join([str(rect) for rect in invalid_rectangles]),
            )
        log(log.INFO, "Validation succeess")

    def pack(
        self,
        use_sheet_in_row: bool = False,
        pack_algo: pack_algo.PackingAlgorithm = skyline.SkylineMwflWm,
    ):
        """Place rectangles on bin area and creating image

        Args:
            use_sheet_in_row (bool, optional): Extra sheet height will be added
                to current sheet height. Defaults to False.
        """

        log(log.INFO, "Prepare to pack rectangles")

        not_placed_rectangles = [
            sorted([float(rect[0]), float(rect[1])]) for rect in self.rectangles
        ]

        log(log.INFO, "Init new packer instance")
        # PackingBin.Global looks good too
        self.packer = newPacker(
            pack_algo=pack_algo, bin_algo=PackingBin.BFF, sort_algo=SORT_SSIDE
        )

        if use_sheet_in_row:
            log(log.INFO, "Add bin")
            self.packer.add_bin(*self.bins[0])
        else:
            for bin_sizes in self.bins:
                log(log.INFO, "Add bin")
                self.packer.add_bin(bin_sizes[0], bin_sizes[1])

        log(log.INFO, "Add rectangles")
        for rect in not_placed_rectangles:
            rect = [
                rect[0] + self.blade_size * 2,
                rect[1] + self.blade_size * 2,
            ]
            self.packer.add_rect(rect[0], rect[1])

        log(log.INFO, "Pack rectangles")
        self.packer.pack()

        for bin in self.packer:
            bin.width -= self.blade_size * 2
            bin.height -= self.blade_size * 2
            log(log.INFO, "Generate result for bin [%s]", bin)

            bin_result = {
                "bin": bin,
                "sizes": [
                    bin.width,
                    bin.height,
                ],
                "rectangles": [],
                "used_area": 0,
                "wasted_area": 0,
                "image": None,
                "max_y_coordinate": 0,
            }
            for rect in bin:
                # remove spacing between artworks and sheet borders
                rect.x -= self.blade_size
                rect.y -= self.blade_size

                if (
                    bin_result["max_y_coordinate"]
                    < rect.y + rect.height - self.blade_size
                ):
                    bin_result["max_y_coordinate"] = (
                        rect.y + rect.height - self.blade_size
                    )
                rect = sorted(
                    [
                        rect.width - self.blade_size * 2,
                        rect.height - self.blade_size * 2,
                    ]
                )
                bin_result["rectangles"].append(rect)
                not_placed_rectangles.remove(rect)
                bin_result["used_area"] += (rect[0] + self.blade_size * 2) * (
                    rect[1] + self.blade_size * 2
                )
            bin_result["wasted_area"] = bin.width * bin.height - bin_result["used_area"]
            self._result["bins"].append(bin_result)

        self._result["not_placed_rectangles"] = not_placed_rectangles

        if self._result["not_placed_rectangles"]:
            if use_sheet_in_row:
                self.bins[0][1] -= self.blade_size * 2
                self.bins[0][1] = int(
                    ((self.bins[0][1]) / self.bins_in_row) * (self.bins_in_row + 1)
                )
                self.bins[0][1] += self.blade_size * 2
                self.bins_in_row += 1
            else:
                self.bins.append(self.bins[0])

            self.reset(self.bins_in_row)
            self.pack(use_sheet_in_row, pack_algo)

    def generate_image_for_bin(self, bin: object, color_chema: dict):
        """Generate image using bin data

        Args:
            bin (object): rectpack bin object

        Returns:
            PIL.Image.Image: generated image with rectangles on bin area
        """
        log(log.INFO, "Generate image for bin [%s]", bin)

        if self.is_sizes_equals:
            bin.width -= 1
        larger_side = max([bin.width, bin.height])
        scale = conf.RECT_PACK_IMG_MAX_SIDE_SIZE / larger_side
        scale *= max([bin.width, bin.height]) / min([bin.width, bin.height])

        bin_width = int(bin.width * scale)
        bin_height = int(bin.height * scale)
        img = Image.new("RGB", (bin_width, bin_height), conf.COLOR_WHITE)

        img_draw = ImageDraw.Draw(img)

        for rect in bin:
            rect_in_color_chema = str(sorted([rect.width, rect.height]))
            rect_color = color_chema.get(rect_in_color_chema)
            if not rect_color:
                color = generate_color_hex()
                color_chema[rect_in_color_chema] = color
                rect_color = color

            rectangle = [
                (rect.x * scale, rect.y * scale),
                ((rect.x + rect.width) * scale, (rect.y + rect.height) * scale),
            ]
            img_draw.rectangle(
                rectangle,
                outline=conf.COLOR_WHITE if self.blade_size else conf.COLOR_BLACK,
                fill=conf.COLOR_WHITE if self.blade_size else rect_color,
            )
            if self.blade_size:
                rectangle = [
                    (
                        (rect.x + self.blade_size) * scale,
                        (rect.y + self.blade_size) * scale,
                    ),
                    (
                        (rect.x + rect.width - self.blade_size) * scale,
                        (rect.y + rect.height - self.blade_size) * scale,
                    ),
                ]
                img_draw.rectangle(
                    rectangle,
                    outline=conf.COLOR_BLACK,
                    fill=rect_color,
                )

        shape = [(bin_width - 1, bin_height - 1), 0, 0]
        img_draw.rectangle(shape, outline=conf.COLOR_BLACK)

        return img
