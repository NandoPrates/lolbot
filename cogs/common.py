"""
The MIT License (MIT)

Copyright (c) 2018 tilda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
# etc data
version = '3.0'
ua_text = 'lolbot/{} - https://lolbot.lmao.tf'.format(version)
user_agent = {
    'User-Agent': ua_text
}


# Dummy class, holds data
# This forms a "object"
# When used, you can now
# hold data inside the variable
# you attached the class to.
# Magic!
class Dummy:
    pass


def setup(bot):
    # Setup a bot emote register, to store emojis for use
    # e.g. notcheck
    bot.emoji = Dummy()
    if bot.config['beta']:
        version = f'{version}b'
        ua_text = f'lolbot/{version} - https://lolbot.lmao.tf'
    else:
        pass
