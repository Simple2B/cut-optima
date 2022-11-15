from rectpack import newPacker, guillotine
from PIL import Image, ImageDraw


class RectPacker:
    def __init__(self, blade_size: int = 0):
        self.packer = newPacker(pack_algo=guillotine.GuillotineBssfMaxas)
        self.bins = []
        self.rectangles = []
        self.blade_size = blade_size
        self.result = {
            "not_placed_rectangles": [],
            "bins": [],
        }

    def add_bin(self, width: int, height: int):
        self.bins.append([width, height])

    def add_rectangle(self, width: int, height: int):
        self.rectangles.append(sorted([width, height]))

    def validate_rectangles(self):
        if not self.bins:
            raise ValueError("Bins not found")
        elif not self.rectangles:
            raise ValueError("Rectangles not found")
        invalid_rectangles = []

        for rect in self.rectangles:
            rect = sorted(rect)
            fit_in_bins = []
            for bin in self.bins:
                bin = sorted(bin)
                fit_in_bins.append(
                    rect[0] + self.blade_size * 2 < bin[0]
                    and rect[1] + self.blade_size * 2 < bin[0]
                )
            if not any(fit_in_bins):
                invalid_rectangles.append(rect)

        if invalid_rectangles:
            raise ValueError(f"Found invalid rectangle(s): {invalid_rectangles}")

    def pack(self):
        for bin in self.bins:
            self.packer.add_bin(*bin)
        for rect in self.rectangles:
            rect = [
                rect[0] + self.blade_size * 2,
                rect[1] + self.blade_size * 2,
            ]
            self.packer.add_rect(*rect)

        self.packer.pack()

        not_placed_rectangles = [sorted(rect) for rect in self.rectangles]
        for bin in self.packer:
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
                bin_result["used_area"] += rect[0] * rect[1]
            bin_result["wasted_area"] = bin.width * bin.height - bin_result["used_area"]

            self.result["bins"].append(bin_result)

            bin_result["image"] = self.generate_image_for_bin(bin)

        self.result["not_placed_rectangles"] = not_placed_rectangles

    def generate_image_for_bin(self, bin):
        shape = [(bin.width, bin.height), 0, 0]

        img = Image.new("RGB", (bin.width, bin.height), "white")

        img_draw = ImageDraw.Draw(img)
        img_draw.rectangle(shape, outline="black")

        for rect in bin:
            rectangle = [
                (rect.x, rect.y),
                (rect.x + rect.width, rect.y + rect.height),
            ]
            img_draw.rectangle(
                rectangle,
                outline="white" if self.blade_size else "black",
                fill="white" if self.blade_size else "#efe6e6",
            )
            if self.blade_size:
                rectangle = [
                    (rect.x + self.blade_size, rect.y + self.blade_size),
                    (
                        rect.x + rect.width - self.blade_size,
                        rect.y + rect.height - self.blade_size,
                    ),
                ]
                img_draw.rectangle(
                    rectangle,
                    outline="black",
                    fill="#efe6e6",
                )
        return img
