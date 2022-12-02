from rectpack import newPacker, guillotine
from PIL import Image, ImageDraw

from config import BaseConfig as conf
from app.logger import log


class RectPacker:
    def __init__(self, blade_size: int = 0):
        """Init RectPacker instance with rectpack.racker object to
        find the optimal arrangement of rectangles on bin area and show it
        on image

        Args:
            blade_size (int, optional): Value that will be added
            to each side of rectangle. Defaults to 0.
        """
        self.packer = newPacker(pack_algo=guillotine.GuillotineBssfMaxas)
        self.bins = []
        self.rectangles = []
        self.blade_size = blade_size
        self.result = {
            "not_placed_rectangles": [],
            "bins": [],
        }

    def reset(self):
        """Remove all results"""
        self.packer = newPacker(pack_algo=guillotine.GuillotineBssfMaxas)
        self.result = {
            "not_placed_rectangles": [],
            "bins": [],
        }

    def add_bin(self, width: int, height: int):
        """Add bin to bins list

        Args:
            width (int): bin width
            height (int): bin height
        """
        log(log.INFO, "Add bin [%s]", [width, height])
        self.bins.append([width, height])

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
                    rect[0] + self.blade_size * 2 <= bin[0]
                    and rect[1] + self.blade_size * 2 <= bin[1]
                )
            if not any(fit_in_bins):
                invalid_rectangles.append(rect)

        if invalid_rectangles:
            log(log.ERROR, "Found invalid rectangle(s): [%s]", invalid_rectangles)

            raise ValueError(
                "Found invalid rectangle(s): %s"
                % ", ".join([str(rect) for rect in invalid_rectangles]),
            )
        log(log.INFO, "Validation succeess")

    def pack(self):
        """Place rectangles on bin area and creating image"""
        log(log.INFO, "Prepare to pack rectangles")

        for bin in self.bins:
            self.packer.add_bin(*bin)
        for rect in self.rectangles:
            rect = [
                rect[0] + self.blade_size * 2,
                rect[1] + self.blade_size * 2,
            ]
            self.packer.add_rect(*rect)

        log(log.INFO, "Prepare to pack rectangles")
        self.packer.pack()

        not_placed_rectangles = [
            sorted([float(rect[0]), float(rect[1])]) for rect in self.rectangles
        ]
        for bin in self.packer:
            log(log.INFO, "Generate result for bin [%s]", bin)
            bin_result = {
                "sizes": [bin.width, bin.height],
                "rectangles": [],
                "used_area": 0,
                "wasted_area": 0,
                "image": None,
            }
            for rect in bin:
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

            self.result["bins"].append(bin_result)

            bin_result["image"] = self.generate_image_for_bin(bin)

        self.result["not_placed_rectangles"] = not_placed_rectangles

        if self.result["not_placed_rectangles"]:
            self.bins.append(self.bins[0])
            self.reset()
            self.pack()

    def generate_image_for_bin(self, bin: object):
        """Generate image using bin data

        Args:
            bin (object): rectpack bin object

        Returns:
            PIL.Image.Image: generated image with rectangles on bin area
        """
        log(log.INFO, "Generate image for bin [%s]", bin)

        larger_side = max([bin.width, bin.height])
        scale = conf.RECT_PACK_IMG_MAX_SIDE_SIZE / larger_side

        bin_width = int(bin.width * scale)
        bin_height = int(bin.height * scale)
        img = Image.new("RGB", (bin_width, bin_height), conf.COLOR_WHITE)

        img_draw = ImageDraw.Draw(img)

        for rect in bin:
            rectangle = [
                (rect.x * scale, rect.y * scale),
                ((rect.x + rect.width) * scale, (rect.y + rect.height) * scale),
            ]
            img_draw.rectangle(
                rectangle,
                outline=conf.COLOR_WHITE if self.blade_size else conf.COLOR_BLACK,
                fill=conf.COLOR_WHITE if self.blade_size else conf.COLOR_GREY,
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
                    fill=conf.COLOR_GREY,
                )

        shape = [(bin_width - 1, bin_height - 1), 0, 0]
        img_draw.rectangle(shape, outline=conf.COLOR_BLACK)

        return img
