# app.py

from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

api_key = "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"
openai.api_key = api_key

provided_script = """
"[0.60 - 1.81]: So what, um...\n",
            "[2.42 - 6.81]: So we'll start with the end bit of a game.\n",
            "[7.02 - 9.62]: There we go, hopefully most of you.\n",
            "[9.68 - 13.27]: Recognize that war let's it's out fairly soon for my friends at Sony\n",
            "[13.30 - 13.80]: Thank you.\n",
            "[13.97 - 15.02]: Thank you.\n",
            "[15.06 - 15.74]: Thank you.\n",
            "[16.22 - 18.09]: Um...\n",
            "[18.19 - 20.50]: That's an image from a game.\n",
            "[20.52 - 26.54]: To be honest, that's probably a mock-up. I suspect that's not a real screen grab, but it's increasingly\n",
            "[26.56 - 28.98]: difficult to tell with the latest hardware.\n",
            "[28.99 - 31.24]: It's a pretty nice image either way.\n",
            "[31.55 - 40.38]: So what are we looking at there? What is an image from a game? What does it consist of?\n",
            "[41.58 - 57.75]: What are the key, the building blocks of it if you like? Yeah? Models. Models, yeah, okay. What are models made of? Polygons. Polygons, there we go. Yeah, so everything in there. 3D models made out of 2D polygons put together.\n",
            "[57.76 - 59.45]: in a 3D world.\n",
            "[59.90 - 63.64]: But that's not what we can see there, is it? That's a 2D image.\n",
            "[63.75 - 65.37]: So what's the image made of?\n",
            "[65.39 - 66.10]: Thank you. Thank you.\n",
            "[66.46 - 66.93]: Thank you.\n",
            "[67.58 - 68.00]: Yeah.\n",
            "[68.01 - 69.99]: Pixels, there we go.\n",
            "[70.03 - 70.62]: Thank you.\n",
            "[70.74 - 71.09]: Thank you.\n",
            "[71.10 - 73.18]: pixels at every\n",
            "[73.25 - 85.52]: every spot if you like on a screen has an RGB value and that's effectively what we're looking at. When you're sat at home playing World of War, when that comes out, you've got a...\n",
            "[85.54 - 87.61]: to the telly\n",
            "[87.68 - 95.15]: displaying a 2D image which is built from these 3D models which have been animated, put into the world.\n",
            "[95.39 - 95.99]: time.\n",
            "[96.07 - 104.96]: Hopefully highly enjoyable games or any boring games. There's plenty of them around as well And this course this module I should say\n",
            "[105.12 - 108.34]: Really the decay of it, the decay of the...\n",
            "[108.78 - 113.51]: of the lectures and the exam really is how\n",
            "[113.55 - 121.14]: do we turn those 3D models created by artists\n",
            "[121.18 - 122.94]: into that 2D.\n",
            "[123.12 - 123.78]: image.\n",
            "[123.84 - 134.54]: which is moving, it's in real time, has to react, you press jump, you want to get the jump on the screen. How does that happen in real time? What algorithms do we use?\n",
            "[134.59 - 139.07]: to make that happen. And that's really what the core of this module is.\n",
            "[139.20 - 140.60]: is all about.\n",
            "[141.26 - 148.59]: We'll give you some practice in doing that. We'll be using Unity, which is an industry standard engine, to do that.\n",
            "[148.70 - 155.80]: But all the lectures are about, they're not really about the, well they're not at all about the implementation.\n",
            "[155.81 - 158.08]: in unity about what's going on.\n",
            "[158.14 - 165.19]: on the hardware. Why is the unit doing the thing it does in order to get those screens running as fast as possible?\n",
            "[166.40 - 172.47]: So just I guess a reminder, I'm sure you are reasonably aware of this.\n",
            "[172.86 - 181.58]: a Pixar movie or Avengers Endgame or whatever it is, if there's all this computer-generated imagery.\n",
            "[181.73 - 190.29]: in all his fantastic movies these days. Pixar famously devoted 36 hours to rendering each and every frame.\n",
            "[190.38 - 197.86]: What I mean by rendering a frame, so we've got those 3D models in the scene, we're going to go through that process of turning...\n",
            "[197.92 - 198.70]: each.\n",
            "[198.78 - 200.72]: each fragment to the image.\n",
            "[200.75 - 208.51]: The big thing that they spend the time on is getting the lighting right. There's an awful lot of work who isn't delighting. So you have your models, you can color them in.\n",
            "[208.75 - 214.78]: how the lid within the scene is well most of the time takes place. And that's really why...\n",
            "[214.82 - 216.86]: whatever the latest Pixar movie.\n",
            "[216.86 - 222.14]: is look so much better than whatever, well, the Cold War, Iraq for example.\n",
            "[222.62 - 224.94]: So, next time, sorry.\n",
            "[224.98 - 230.06]: Pixar Famously spends 36 hours on every single frame of their movies.\n",
            "[230.12 - 244.37]: They do them in parallel, they don't just do one and then 36 hours later they move on to the next one. They do lots of them in parallel, but every frame gets 36 hours of processing time, effectively turning those 3D models into a 2D image for the screen.\n",
            "[244.56 - 244.92]: Thank you.\n",
            "[244.95 - 245.44]: Thank you.\n",
            "[245.50 - 246.87]: Come on, do that in games.\n",
            "[246.91 - 253.73]: We've got 33 milliseconds to do exactly the same thing as Pixar have 36 hours to do.\n",
            "[255.45 - 255.83]: Thank you.\n",
            "[256.10 - 258.23]: So we've got it pretty efficient there really.\n",
            "[258.36 - 258.70]: Thank you.\n",
            "[258.86 - 259.26]: Thank you.\n",
            "[259.54 - 262.38]: Why do we only have 33 milliseconds?\n",
            "[263.20 - 263.89]: Thank you. Thank you.\n",
            "[264.59 - 266.08]: \n",
            "[266.18 - 266.62]: you\n",
            "[266.82 - 269.75]: Get 60 frames a second.\n",
            "[269.86 - 275.61]: OK, but why can't we do lots of them in parallel, so spend a minute on each one? Is this going to change?\n",
            "[275.75 - 285.27]: It's gonna change has to react what the players doing you press jump you want Mario to jump You don't want him going off and coming back 36 hours later saying yeah, I've tuned that\n",
            "[285.65 - 291.82]: So, it's really similar techniques used with Pixar as with Nintendo.\n",
            "[292.00 - 294.02]: But the key here is to get.\n",
            "[294.18 - 314.02]: Our rendering process is working as fast as possible while still looking amazing. You shouldn't be cutting corners just to get speed. It has to still look great. Hopefully one of the things we get across during this lecture series is that balancing act. You can always chuck in more fidelity, make it look greater. That's going to bring the frame rate down.\n",
            "[314.40 - 317.85]: So you've got to find ways of maintaining the visual quality.\n",
            "[318.14 - 321.12]: and also the frame rate.\n",
            "[321.26 - 327.67]: You play some of these big open world games, you go somewhere, drops down to 20 frames per second, you go, no, like that.\n",
            "[327.70 - 343.30]: And if you're in virtual reality, really you've got to be 120 frames per second, because you want this eye to be going at 60, and this eye to be going at 60. You end up in the same scene twice. So you've got to be even faster on virtual reality applications.\n",
            "[343.30 - 344.42]: Thank you.\n",
            "[344.53 - 345.22]: Thank you.\n",
            "[345.38 - 347.55]: Right, I've forgotten what's next.\n",
            "[347.60 - 364.31]: Yes, so, as I say, the main thing we'll be talking about through the lecture series is how do we do that in real time? How do we turn those 3D models into a 2D image at a rate of 60 frames per second? What's going on on the hardware? We're going to talk about how the GPU...\n",
            "[364.36 - 385.43]: does this and how we as programmers harness the GPU to achieve what we want to do. So we can get fantastic images like Mario there. I'm a bit of a Nintendo fan so there will be a few pictures of Mario and Zelda throughout. I'm guessing that are mostly PC players. No, a few shaking heads. Who's a PC game player?\n",
            "[385.61 - 392.14]: Yeah, and with Hans Guur. Why do I hate PC game development as a game developer?\n",
            "[392.19 - 393.02]: Thank you.\n",
            "[393.06 - 393.42]: Thank you.\n",
            "[393.69 - 418.94]: Because they're all different.\n",
            "[418.99 - 427.13]: As mentioned this lecture is just kind of an introduction to this whole process. So we'll give you an overview\n",
            "[427.19 - 428.64]: of each step.\n",
            "[428.70 - 433.77]: along the way, give a sense of what the module is and what's expected from the coursework as well.\n",
            "[433.79 - 442.04]: So, as was mentioned by my friend at the back there, our models in the game, the 3D models...\n",
            "[442.07 - 455.86]: They're built by from a sequence of polygons, typically triangles. So there's Mario again. We all know he's built up a mesh of triangles, the quartz here.\n",
            "[455.98 - 457.82]: Of course, just two triangles.\n",
            "[457.85 - 459.09]: Put together.\n",
            "[459.82 - 461.98]: It's actually it's more\n",
            "[462.18 - 468.08]: abstract than that. The models aren't really sets of triangles, they're sets of points in space.\n",
            "[468.18 - 477.32]: And those points in space are connected together in polygon. It's usually in triangles. You can get a string of triangles to put together to make the model so item.\n",
            "[477.44 - 480.62]: A point in space is known as a vertex.\n",
"""

def query_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": provided_script},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_message = request.form['msg']
    bot_response = query_openai(user_message)
    return jsonify(bot_response)

@app.route('/')
def index():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
