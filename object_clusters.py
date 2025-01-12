class ObjectClusters:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # divide screen into 6 equal sized blocks
        self.block_width = self.screen_width // 3
        self.block_height = self.screen_height // 2

        # number of blocks to use in array
        self.blocks_x = self.screen_width // self.block_width - 1
        self.blocks_y = self.screen_height // self.block_height - 1

    def object_position_in_grid(self, center_x, center_y):
        # returns the position in 2x3 grid for the object
        column = center_x // self.block_width
        row = center_y // self.block_height

        # if object is at the edge of the screen, need to subtract one
        # otherwise results in out of bounds
        if center_x >= self.screen_width: column -= 1
        if center_y >= self.screen_height: row -= 1

        return int(column), int(row)
    
    def get_block_dimensions(self):
        return self.blocks_x, self.blocks_y

    # takes in a 2x3 array 
    def place_object_to_grid(self, center_x, center_y, blocks_grid):
        obj_column, obj_row = self.object_position_in_grid(center_x, center_y)
        blocks_grid[obj_column][obj_row] += 1