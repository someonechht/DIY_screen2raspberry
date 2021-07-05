import pyglet
from server import server
import threading

#start server
computer = server()
computer.start_server()


window = pyglet.window.Window()
label = pyglet.text.Label(computer.ip,
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
      
    if computer.img != None:
        raw = computer.img.tobytes()
        image = pyglet.image.ImageData(computer.img.width, computer.img.height, 'RGB', raw, pitch=-computer.frame_width * 3)
        image.blit(0,0)
    



pyglet.app.run()
computer.stop_server()
