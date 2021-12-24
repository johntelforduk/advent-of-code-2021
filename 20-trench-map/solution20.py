# Solution to day 20 of AOC 2021, Trench Map
# https://adventofcode.com/2021/day/20


class Image:

    def __init__(self, start: str):
        self.grid = {}
        self.background = '.'

        x, y = 0, 0
        for row in start.split('\n'):
            x = 0
            for col in row:
                self.grid[(x, y)] = col
                x += 1
            y += 1

        self.min_x, self.min_y = 0, 0

        # Deal with some gateposts!
        self.max_x, self.max_y = x - 1, y - 1

    def pixel(self, x: int, y: int) -> str:
        """For parm coords. Return the pixel, '.' for off and '#' for on."""
        if (x, y) in self.grid:
            return self.grid[(x, y)]
        return self.background

    def print_image(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                print(self.pixel(x, y), end='')
            print()
        print()

    def nine_pixels_to_denary(self, p: str) -> int:
        """For parm string of nine pixels, return its deneray value."""
        return int(p.replace('.', '0').replace('#', '1'), 2)

    def pixel_coord_to_denary(self, x, y) -> int:
        """For pixel at parm coords. Return the denary value for the 3x3 grid around it."""
        pixel_str = ''
        for yi in range(y - 1, y + 2):
            for xi in range(x - 1, x + 2):
                pixel_str += self.pixel(xi, yi)

        pixel_binary = self.nine_pixels_to_denary(pixel_str)
        return pixel_binary

    def denery_enhance(self, algo: str, num: int) -> str:
        """For parm decimal number for a pixel, return the enhance pixel string, '.' or '#'."""
        return algo[num]

    def enhance(self, algo: str):
        new_grid = {}

        # Move boundaries out by 1 position in all directions.
        self.min_x -= 1
        self.min_y -= 1
        self.max_x += 1
        self.max_y += 1

        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                new_grid[x, y] = self.denery_enhance(algo, self.pixel_coord_to_denary(x, y))

        # Deal with the infinite background.
        background_denary = self.nine_pixels_to_denary(9 * self.background)
        self.background = self.denery_enhance(algo, background_denary)

        self.grid = new_grid

    def count_lit(self) -> int:
        count = 0
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if self.pixel(x, y) == '#':
                    count += 1
        return count


test_str = """#..#.
#....
##..#
..#..
..###"""
test_algo = '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#'

test_image = Image(test_str)
assert test_image.nine_pixels_to_denary('.........') == 0
assert test_image.nine_pixels_to_denary('#########') == 511
assert test_image.nine_pixels_to_denary('...#...#.') == 34

assert test_image.denery_enhance(test_algo, 0) == '.'
assert test_image.denery_enhance(test_algo, 511) == '#'
assert test_image.denery_enhance(test_algo, 34) == '#'

f = open('input.txt')
t = f.read()
f.close()

raw_algorithm, raw_image = t.split('\n\n')

my_image = Image(raw_image)

for i in range(50):
    my_image.enhance(raw_algorithm)
    my_image.print_image()

print(my_image.count_lit())
