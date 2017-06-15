from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
import docker

class DockerListButton(ListItemButton):
    pass

class DockerDB(BoxLayout):
    image_text_input = ObjectProperty()
    container_text_input = ObjectProperty()
    docker_list = ObjectProperty()

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