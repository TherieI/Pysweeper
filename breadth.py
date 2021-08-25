self.frontier = Queue()
self.frontier.put(start)

self.came_from = dict()
self.came_from[start] = None

def get_all_paths(self, visual_scan=True):
    found = False
    while not self.frontier.empty():
        sleep(settings.algorithm_speed)
        current = self.frontier.get()
        if current == self.end:
            found = True
            break
        for cell in self.neighbors(current, cardinal_only=settings.neighbor_type):
            if visual_scan and not cell.is_fixed():
                cell.cont = Contents.SCANNED
            if cell not in self.came_from:
                self.frontier.put(cell)
                self.came_from[cell] = current
    if not found:
        return None
    return self.came_from