"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
import os

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask session features

app.secret_key = os.environ["KEY"]

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id): #when URL routing with details, an addition to the link, we have to pass in the variable as a parameter to the view function
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id) 

    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    if "cart" in session:
        cart = session["cart"]
    else:
        cart = session['cart'] = {}
    
    cart[melon_id] = cart.get(melon_id, 0) + 1

    #print(cart) - temporary testing to make sure melon was added to cart 

    flash("Melon successfully added to cart.")

    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""
    
    #keep track of the total cost of the order, running tally
    order_total = 0

    #list to hold melon objects corresponding to the melon_id's in the cart
    cart_list = []

    #get cart dict out of the session, including if an empty one
    cart = session.get("cart", {})
    
    #loop over the cart dict 
    for melon_id, quantity in cart.items():
        #get melon object corresponding to id
        melon = melons.get_by_id(melon_id)

        total_cost = quantity * melon.price #subtotal: get cost with quantity times price
        order_total += total_cost #for total: adding cost to total cost for running tally

        #add quan and cost as attribute to Melon object 
        melon.quantity = quantity
        melon.total_cost = total_cost

        #add the Melon object to the list 
        cart_list.append(melon)

    #pass cart and total to Jinja template 
    return render_template("cart.html", cart=cart_list, order_total=order_total)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site: Find the user's login credentials located in the 'request.form'
    
    dictionary, look up the user, and store the user in the session.
    """

    email = request.form.get('email') #request/pull email from form
    password = request.form.get('password') #request/pull password from form

    user = customers.get_by_email(email) #user helper function in customers.py (w/ Class) to see if the user is already in the site's data based on the email address, per the helper function I wrote in that customers.py file 

    #handling logic
    if not user: #if not user in the site's system, then they can't log in and need to try again 
        flash("No customer with that email found.")
        redirect('/login')
        
    if user.password != password: #if there is a user with that email address, now check the password to what's already in the site data
        flash("Incorrect password.")
        redirect('/login')
    
    #finally, if not one of those above, where it isn't the user/user data matching what the data already stored in the site, then the email and password are correct, and the user is logged in and their information is stored in the session - by email, because that's how we're looking up users on this app, since that's what will no doubt be the unique identifier from user to user (name could be the same, pw could be the same, but only one email is created with those characters in user in general)
    session["logged_in_customer_email"] = user.email
    flash("Logged in") #letting the user know and (re)setting the session (with the user's info., then the methods and attributes can be accessed throughout the program)
    return redirect('/melons') #user is now redirected to see all the melons, to choose which to add to their cart => $$

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
