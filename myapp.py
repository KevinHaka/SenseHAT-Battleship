from flask import Flask, render_template, request, session, g, url_for, redirect
from sense_emu import SenseHat
import random

s = SenseHat()
s.clear()

app = Flask(__name__)
app.secret_key = "1234"

class C:
    red = [200, 0, 0]
    green = [0,200,0]
    blue = [0, 0, 200]


    black=[0,0,0]
    red_hit = [200, 200, 0]
    blue_hit = [0, 200, 200]

shipmap=[C.green]*10+[C.black]*54
counter = {}

users= []
users.append([1, 'Giannis','kodikos_Gianni'])
users.append([2, 'Maria','kodikos_Marias'])
users.append([3, 'kev', 'kev'])
users.append([4, 'in', 'in'])


@app.route('/')
def homepage():
    if not g.user:
        return redirect(url_for('logme'))
    
    return render_template('index.html')

@app.route('/logme', methods=['POST','GET'])
def logme():
    session.pop('user_id', None)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        for user in users:
            if user[1]==username and user[2]==password:
                session['user_id'] = user[0]
                
                return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/sense')
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    
    return render_template('info.html')

@app.route('/ships', methods=['POST','GET'])
def ships():
    if not g.user:
        return redirect(url_for('logme'))

    if request.method == 'POST':
        horizontal = int(request.form['horizontal'])
        
        if horizontal > 7:
            random.shuffle(shipmap)
            s.set_pixels(shipmap)
        else:
            vertical = int(request.form['vertical'])
            s.set_pixel(horizontal, vertical, C.blue)
    
    else: s.clear()
    
    return render_template('ships.html')

@app.route('/bonus_ships', methods=['POST','GET'])
def bonus_ships():
    if not g.user:
        return redirect(url_for('logme'))
    
    message = {}
    user_color = f"Your color is {'RED' if (session['user_id'] % 2 == 0) else 'BLUE'}"

    if request.method == 'POST':
        horizontal = request.form['horizontal']
        vertical = request.form['vertical']
        
        if isnum(horizontal):
            horizontal = int(horizontal)
            
            if (horizontal < 0) or (horizontal > 7):
                random.shuffle(shipmap)
                s.set_pixels(shipmap)
            
            elif isnum(vertical):
                vertical = int(vertical)
        
                if (vertical < 0) or (vertical > 7):
                    message = "Vertical value must be between 0 and 7"
                    
                elif C.green in s.get_pixels():
                    match s.get_pixel(horizontal, vertical):
                        case C.black:
                            color = C.red if (session["user_id"] % 2 == 0) else C.blue
                            s.set_pixel(horizontal, vertical, color)
                        case C.green:
                            color = C.red_hit if (session["user_id"] % 2 == 0) else C.blue_hit
                            s.set_pixel(horizontal, vertical, color)
                        case C.red | C.red_hit:
                            message = f"The position ({horizontal}, {vertical}) is already taken by the RED player"
                        case C.blue | C.blue_hit:
                            message = f"The position ({horizontal}, {vertical}) is already taken by the BLUE player"                        
                    
                    if counter['green'] == 0:
                        message = "The game is over"

                else:
                    message = "Please start the game before selecting a position"
                
            else:
                message = "Please complete all fields"
    
    counter['red'] = s.get_pixels().count(C.red)
    counter['green'] = s.get_pixels().count(C.green)
    counter['blue'] = s.get_pixels().count(C.blue)
    counter['red_hit'] = s.get_pixels().count(C.red_hit)
    counter['blue_hit'] = s.get_pixels().count(C.blue_hit)
    
    return render_template('bonus_ships.html', message=message, user_color=user_color, counter=counter)

@app.route('/clear')
def clear():
    if not g.user:
        return redirect(url_for('logme'))
    
    s.clear()
    return redirect(url_for('bonus_ships'))

@app.before_request
def before_request():
    g.user=None
    
    if 'user_id' in session:
        for user in users:
            if user[0] == session['user_id']:
                g.user = user
                g.s = s
                
@app.context_processor
def a_processor():
    def roundv(value,digits):
        
        return round(value,digits)
    return {'roundv':roundv}

def isnum(z):
    if z != "":
        if z[0] in ["+", "-"]: z = z[1:]
        
    return z.isdigit()
    

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
