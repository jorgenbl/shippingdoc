from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import docker
from datetime import datetime
import time

class DockerListButton(ListItemButton):
    pass

class DockerRecord(Label):
    pass

class TableHeader(Label):
    pass

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.get_running_containers()
        self.display_running_containers()


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

    def get_running_containers(self):
        self.data = [{'CONTAINER ID': 'CONTAINER ID', 'IMAGE': 'IMAGE', 'CREATED': 'CREATED', 'NAME': 'NAME'}]

        # Time initializations
        fmt = '%Y-%m-%dT%H:%M:%S'
        now = datetime.strptime(datetime.now().isoformat().split(".")[0], fmt)
        now_ts = time.mktime(now.timetuple())


        client = docker.from_env()
        for container in client.containers.list():
            container_row = {}
            containerDict = container.__dict__
            container_row["CONTAINER ID"] = containerDict["attrs"]["Config"]["Hostname"]
            container_row["IMAGE"] = containerDict["attrs"]["Config"]["Image"]
            created = datetime.strptime(containerDict["attrs"]["Created"].split(".")[0], fmt)
            created_ts = time.mktime(created.timetuple())
            container_row["CREATED"] = self.display_time(int(now_ts-created_ts))
            container_row["NAME"] = containerDict["attrs"]["Name"].split("/")[1]
            self.data.append(container_row)
        

    def display_running_containers(self):
        self.clear_widgets()
        for i in xrange(len(self.data)):
            if i < 1:
                row = self.create_table_header(i)
            else:
                row = self.create_table(i)
            for item in row:
                self.add_widget(item)


    def create_table_header(self, i):
        first_column = TableHeader(text=self.data[i]['CONTAINER ID'])
        second_column = TableHeader(text=self.data[i]['IMAGE'])
        third_column = TableHeader(text=self.data[i]['CREATED'])
        fourth_column = TableHeader(text=self.data[i]['NAME'])
        return [first_column, second_column, third_column, fourth_column]

    def create_table(self, i):
        first_column = DockerRecord(text=self.data[i]['CONTAINER ID'])
        second_column = DockerRecord(text=self.data[i]['IMAGE'])
        third_column = DockerRecord(text=self.data[i]['CREATED'])
        fourth_column = DockerRecord(text=self.data[i]['NAME'])
        return [first_column, second_column, third_column, fourth_column]

class DockerDB(BoxLayout):
    image_text_input = ObjectProperty()
    container_text_input = ObjectProperty()
    #cols = NumericProperty()

    def find_container(self):
        # Get the container name from textInputs
        container = self.container_text_input.text

        # Clear Docker List
        del self.docker_list.adapter.data[:]

        # Search through available containers and replace listview with result
        self.docker_list.adapter.data.extend([container])

        # Reset the listview
        self.docker_list._trigger_reset_populate()

    def find_image(self):
        # Get the image name from textInputs
        # Search through available images and replace listview with result
        # Reset the listview
        self.docker_list._trigger_reset_populate()

    def list_images(self):
        # Get all images and add to listview
        # Reset the listview
        self.docker_list._trigger_reset_populate()

    def list_containers(self):
        # Clear Docker List
        del self.docker_list.adapter.data[:]

        # Get all containers and add to listview
        client = docker.from_env()
        for container in client.containers.list(all=True):
            # Add container to listview
            self.docker_list.adapter.data.extend([container.name])
        
        # Reset the listview
        self.docker_list._trigger_reset_populate()



class ShippingDocApp(App):
    def build(self):
        return DockerDB()

if __name__ == '__main__':
    shippingApp = ShippingDocApp()
    shippingApp.run()