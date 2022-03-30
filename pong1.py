import turtle;
import os;#linux e mac
import winsound;

wn = turtle.Screen();
wn.title("Pong by @Alessandro");
wn.bgcolor("black");
wn.setup(width=800, height=600);
#turns off the screen updates, withoout this the screen will update every time the ball hits the paddle
wn.tracer(0);

score_a = 0;
score_b = 0;


# Paddle A
paddle_a = turtle.Turtle();
paddle_a.speed(0);
paddle_a.shape("square");
paddle_a.color("white");
paddle_a.penup();#no drawing when moving
paddle_a.goto(-350, 0);# Move the paddle with the keyboard
paddle_a.shapesize(stretch_wid=5, stretch_len=1);

# Paddle B
paddle_b = turtle.Turtle();
paddle_b.speed(0);
paddle_b.shape("square");
paddle_b.color("white");
paddle_b.penup();#no drawing when moving
paddle_b.goto(350, 0);
paddle_b.shapesize(stretch_wid=5, stretch_len=1);

# Ball
ball = turtle.Turtle();
ball.speed(0);
ball.shape("square");
ball.color("white");
ball.penup();#no drawing when moving
ball.goto(0, 0);
ball.dx = 0.1;
ball.dy = 0.1;


ballpoint = turtle.Turtle();
ballpoint.speed(0);
ballpoint.shape("circle");
ballpoint.color("red");
ballpoint.shapesize(stretch_wid=0.1, stretch_len=0.1);
ballpoint.penup();#no drawing when moving
ballpoint.goto(paddle_b.xcor(), paddle_b.ycor()-50);

#Pen
pen = turtle.Turtle();
pen.speed(0);
pen.color("white");
pen.penup();
#pen.shape("square");
pen.hideturtle();# hide the cursor
pen.goto(0, 260); # Move the pen to the center of the screen
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"));


#functions
def paddle_a_up():
    y = paddle_a.ycor();
    if (y < 250):
        y += 20;
        paddle_a.sety(y);
    
def paddle_a_down():
    y = paddle_a.ycor();
    if (y > -250):
        y -= 20;
        paddle_a.sety(y);  
    
    
def paddle_b_up():
    y = paddle_b.ycor();
    if (y < 250):
        y += 20;
        paddle_b.sety(y);
    
def paddle_b_down():
    y = paddle_b.ycor();
    if y > -250:
        y -= 20;
        paddle_b.sety(y);      

#keyboard binding
wn.listen();
wn.onkeypress(paddle_a_up, "w");#when the key w is pressed, the function paddle_a_up will be called
wn.onkeypress(paddle_a_down, "s");#when the key s is pressed, the function paddle_a_down will be called
wn.onkeypress(paddle_b_up, "Up");
wn.onkeypress(paddle_b_down, "Down");



#main game loop
while True:
    wn.update();
    ball.sety(ball.ycor() + ball.dy);
    ball.setx(ball.xcor() + ball.dx);
    
    #palla sbatte sul bordo in alto
    if ball.ycor() > 290:
        ball.sety(290);
        ball.dy *= -1;
        #os.system("afplay bounce.wav&");
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC);
    
    if ball.xcor() > 390:
        ball.goto(0, 0);
        ball.dx *= -1;
        score_a += 1;
        pen.clear();
        pen.write( "Player A: " + str(score_a) + "  Player B: " + str(score_b) , align="center", font=("Courier", 24, "normal"));
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC);
    
    #palla sbatte sul bordo in basso
    if ball.ycor() < -290:
        ball.sety(-290);
        ball.dy *= -1;
        #os.system("afplay bounce.wav&");
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC);
        
    if ball.xcor() < -390:
        ball.goto(0, 0);
        ball.dx *= -1;
        score_b += 1;
        pen.clear()
        pen.write( "Player A: {}  Player B: {}".format(score_a,score_b) , align="center", font=("Courier", 24, "normal"));
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC);
    
    if ball.xcor()> 340 and ball.xcor() < 350 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
       # ball.setx(340);
        ball.dx *= -1;
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC);
    if ball.xcor()< -340 and ball.xcor() > -350 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50:
      #  ball.setx(-340);
        ball.dx *= -1;
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC);
        
    
