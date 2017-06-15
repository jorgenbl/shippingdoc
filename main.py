from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import docker
from datetime import datetime
import time
from collections import OrderedDict

class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)


class DockerListButton(ListItemButton):
    pass

class DockerRecord(Label):
    pass

class TableHeader(Label):
    pass

class MyGrid(GridLayout):

    cols = NumericProperty()

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.get_containers()
        self.display_containers()


    def display_time(self, seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
            )
        result = []
    
        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])


    def get_containers(self, all=False):
        self.data = []

        # Time initializations
        fmt = '%Y-%m-%dT%H:%M:%S'
        now = datetime.strptime(datetime.now().isoformat().split(".")[0], fmt)
        now_ts = time.mktime(now.timetuple())


        client = docker.from_env()
        for container in client.containers.list(all):
            container_row = OrderedDict()
            containerDict = container.__dict__
            container_row["CONTAINER ID"] = containerDict["attrs"]["Config"]["Hostname"]
            container_row["IMAGE"] = containerDict["attrs"]["Config"]["Image"]
            created = datetime.strptime(containerDict["attrs"]["Created"].split(".")[0], fmt)
            created_ts = time.mktime(created.timetuple())
            container_row["CREATED"] = self.display_time(int(now_ts-created_ts))
            container_row["NAME"] = containerDict["attrs"]["Name"].split("/")[1]
            self.data.append(container_row)

        try:
            self.cols = len(self.data[0].keys())
        except:
            self.cols = 0        

    def display_containers(self):
        self.clear_widgets()
        row = self.create_table_header(0)
        for item in row:
            self.add_widget(item)
        for i in xrange(len(self.data)):
            row = self.create_table(i)
            for item in row:
                self.add_widget(item)


    def create_table_header(self, i):
        cols = []
        try:
            row_keys = self.data[i].keys()
            for key in row_keys:
                cols.append(TableHeader(text=key))
        except:
            pass
        return cols

    def create_table(self, i):
        cols = []
        try:
            row_keys = self.data[i].keys()
            for key in row_keys:
                cols.append(DockerRecord(text=self.data[i][key]))
        except:
            pass
        return cols

class DockerDB(BoxLayout):
    image_text_input = ObjectProperty()
    container_text_input = ObjectProperty()
    docker_grid = ObjectProperty()

    def find_container(self):
        # Get the container name from textInputs
        container = self.container_text_input.text

        # Clear Docker List
        print self.docker_grid.data
        #self.docker_grid.clear_widgets()
        
        for child in self.docker_grid.children[:]:
            # manipulate the tree. For example here, remove all widgets that have a
            # width < 100
            print(child)
            self.docker_grid.remove_widget(child)

        # Search through available containers and replace listview with result
        #self.docker_list.adapter.data.extend([container])

        # Reset the listview
        #self.docker_grid._trigger_reset_populate()

    def find_image(self):
        # Get the image name from textInputs
        # Search through available images and replace listview with result
        # Reset the listview
        self.docker_list._trigger_reset_populate()

    def list_images(self):
        # Get all images and add to listview
        # Reset the listview
        self.docker_grid.display_containers()

    def list_all_containers(self):
        # Clear Docker List
        for child in self.docker_grid.children[:]:
            print(child)
            self.docker_grid.remove_widget(child)

        # Get all containers and add to grid
        self.docker_grid.get_containers(all=True)
        self.docker_grid.display_containers()



class ShippingDocApp(App):
    def build(self):
        return DockerDB()

if __name__ == '__main__':
    shippingApp = ShippingDocApp()
    shippingApp.run()