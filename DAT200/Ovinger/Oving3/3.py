import turtle as t


def snowflake(length, levels):
    t.pendown()
    for k in range(3):
        snowflake_helper(length, levels)
        t.right(120)


def snowflake_helper(length, levels):
    if levels == 1:
        t.forward(length)
        return
    snowflake_helper(length/3, levels-1)
    t.left(60)
    snowflake_helper(length/3, levels-1)
    t.right(120)
    snowflake_helper(length/3, levels-1)
    t.left(60)
    snowflake_helper(length/3, levels-1)
    

if __name__ == '__main__':
    t.mode("logo")
    t.hideturtle()
    t.tracer(0)
    t.penup()
    t.forward(180)
    t.right(150)
    snowflake(100, 7)
    t.update()
    t.mainloop()
