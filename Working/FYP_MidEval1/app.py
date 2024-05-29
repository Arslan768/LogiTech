from flask import Flask , render_template ,request, redirect, url_for , session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from classes import *
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'DontTellAnyone'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hafizhashimkardar@gmail.com'
app.config['MAIL_PASSWORD'] = 'imbr yhko jjei aapp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)
socketio = SocketIO(app)
connected_transporters = []


class User(db.Model):
    user_id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(200) , nullable = False)
    password = db.Column(db.String(20) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    user_role = db.Column(db.String(200) , nullable = False)
    confirmed = db.Column(db.Boolean , default = False)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    driver_name = db.Column(db.String(50), nullable=False)
    license_number = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)

class Transporter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    transporter_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200) , nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    customer_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)

class Industrialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    industrialist_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    company_address = db.Column(db.String(255), nullable=False)


class ScheduledDelivery(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.user_id') , nullable=False)
    pickup_location = db.Column(db.String(50) , nullable = False)
    destination = db.Column(db.String(50) , nullable = False)
    proposed_amount = db.Column(db.Integer , nullable = False)
    deal_done = db.Column(db.Boolean , default=False)
    vehicle_type = db.Column(db.String(50) , nullable = False)
    weight = db.Column(db.Integer , nullable = False)
    Goods_Description=db.Column(db.String(150) , nullable = False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'proposed_amount': self.proposed_amount,
            'vehicle_type': self.vehicle_type,
            'weight': self.weight,
            'Goods_Description': self.Goods_Description
        }

class BuiltyForm(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.user_id') , nullable=False)
    Builty_No= db.Column(db.String(50) , nullable = False)
    Date= db.Column(db.String(50) , nullable = False)
    pickup_location = db.Column(db.String(50) , nullable = False)
    destination = db.Column(db.String(50) , nullable = False)
    vehicle_no= db.Column(db.String(50) , nullable = False)
    Sender_Name= db.Column(db.String(50) , nullable = False)
    Receiver_Name= db.Column(db.String(50) , nullable = False)
    Driver_Name=db.Column(db.String(50) , nullable = False)
    Driver_Number= db.Column(db.String(50) , nullable = False)
    FreightDecided = db.Column(db.Integer , nullable = False)
    Goods_Description= db.Column(db.String(250) , nullable = False)
    payment_status = db.Column(db.String(10) , nullable=False)
    
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    transporter_id = db.Column(db.Integer, db.ForeignKey('transporter.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    industrialist_id = db.Column(db.Integer, db.ForeignKey('industrialist.id'))
    pickup_city = db.Column(db.String(50), nullable=False)
    delivery_city = db.Column(db.String(50), nullable=False)
    scheduled_date = db.Column(db.String(20), nullable=False)
    actual_delivery_date = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False)

class DeliveryChallan(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id=db.Column(db.Integer, nullable=False)
        DeliveryChallan_No=db.Column(db.Integer, nullable=False)
        Date=db.Column(db.String(50), nullable=False)
        vehicle_no=db.Column(db.String(50), nullable=False)
        Customer_Name=db.Column(db.String(50), nullable=False)
        Transporter_Name=db.Column(db.String(50), nullable=False)
        weight=db.Column(db.Integer, nullable=False)
        Goods_Description=db.Column(db.String(150), nullable=False)
        CheckedBy=db.Column(db.String(50), nullable=False)
        
with app.app_context():
    db.create_all()


def send_notification_to_transporters(delivery_details):
    notification = delivery_details.to_dict()

    # print(connected_transporters)
    # print("SOMETHING")
    print(notification)
    for transporter in connected_transporters:
        socketio.emit('notification', notification, room=transporter)

@app.route('/')
def hello_world():
    return render_template('MainHomepage.html')

@app.route('/LoginPage' , methods = ['GET' , 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('LoginPage.html')
    elif request.method == 'POST':
        entered_email = request.form['email']
        entered_password = request.form['password']
        user = User.query.filter_by(email=entered_email).first()

        if user:
            if entered_password == user.password:
                if user.user_role == 'Industrialist':
                    return redirect(url_for('industrialist_inside_website' , user_id = user.user_id))
                elif user.user_role == 'Transporter':
                    return redirect(url_for('transporter_inside_website' , user_id = user.user_id))
                elif user.user_role == 'Customer':
                    return redirect(url_for('customer_inside_website' , user_id = user.user_id))
            else:
                return render_template('ErrorMessage.html', custom_error_message='INCORRECT PASSWORD' , heading = 'LOGIN ERROR')
        else:
            return render_template('ErrorMessage.html', custom_error_message='USER NOT FOUND' , heading = "LOGIN ERROR")
        
        
        
@app.route('/IndustrialistInsideWebsite/<user_id>' , methods = ['GET' , 'POST'])
def industrialist_inside_website(user_id):
    if request.method == 'GET':
        return render_template('IndustrialistInsideWebsite.html' , user_id = user_id)
    if request.method == 'POST':
        return render_template('IndustrialistInsideWebsite.html' , user_id = user_id)



@app.route('/ScheduleDelivery/<user_id>' , methods = ['GET' , 'POST'])
def schedule_delivery(user_id):
    if request.method == 'GET':
        return render_template('ScheduleDelivery.html' , user_id = user_id)
    elif request.method == 'POST':
        user = User.query.filter_by(user_id = user_id).first()
        pickup_location = request.form['pickup_location']
        destination = request.form['destination']
        proposed_amount = request.form['proposed_amount']
        vehicle_type = request.form['vehicle_type']
        weight = request.form['weight']
        Goods_Description =request.form['Goods']
        sc_delv = ScheduledDelivery(user_id = user_id , pickup_location = pickup_location , destination = destination , proposed_amount = proposed_amount , vehicle_type = vehicle_type , weight = weight,Goods_Description=Goods_Description)
        
        db.session.add(sc_delv)
        db.session.commit()
        
        send_notification_to_transporters(sc_delv)
        return redirect(url_for('industrialist_inside_website' , user_id = user.user_id))
        

@app.route('/BuiltyForm/<user_id>' , methods = ['GET' , 'POST'])
def create_builty_form(user_id):
    if request.method == 'GET':
        return render_template('BuiltyForm.html' , user_id = user_id)
    elif request.method == 'POST':
        user = User.query.filter_by(user_id = user_id).first()
        pickup_location = request.form['PickUp_Point']
        Builty_No = request.form['Builty_No']
        Date=request.form['Date']
        
        destination = request.form['Destination']
        FreightDecided = request.form['FreightDecided']
        vehicle_no = request.form['Vehicle_No']
        Sender_Name= request.form['Sender_Name']
        Receiver_Name= request.form['Receiver_Name']
        Driver_Name= request.form['Driver_Name']
        Driver_Number= request.form['Driver_Number']

        Goods_Description= request.form['Goods']
        payment_status = request.form.get('paid', 'not paid')

        
        builty = BuiltyForm(user_id = user_id ,Builty_No=Builty_No ,Date=Date,pickup_location = pickup_location , destination = destination , vehicle_no=vehicle_no ,Sender_Name=Sender_Name,Receiver_Name=Receiver_Name,Driver_Name=Driver_Name,Driver_Number=Driver_Number, FreightDecided= FreightDecided ,Goods_Description=Goods_Description,payment_status=payment_status)
        
        db.session.add(builty)
        db.session.commit()

        return redirect(url_for('transporter_inside_website' , user_id = user.user_id))
        

@app.route('/DeliveryChallan/<user_id>' , methods = ['GET' , 'POST'])
def create_delivery_challan(user_id):
    if request.method == 'GET':
        return render_template('DeliveryChallan.html' , user_id = user_id)
    elif request.method == 'POST':
        user = User.query.filter_by(user_id = user_id).first()
        
        DeliveryChallan_No = request.form['Delivery_Challan_No']
        Date=request.form['Date']
        
        vehicle_no = request.form['Vehicle_No']
        weight=request.form['weight']
        Customer_Name= request.form['CustomerName']
        Transporter_Name= request.form['Transporter_Name']
        
        Goods_Description= request.form['Goods']
        CheckedBy=request.form['CheckedBy']
        
        delivery = DeliveryChallan(user_id = user_id ,DeliveryChallan_No=DeliveryChallan_No ,Date=Date,vehicle_no=vehicle_no ,Customer_Name=Customer_Name,Transporter_Name=Transporter_Name,weight=weight,Goods_Description=Goods_Description,CheckedBy=CheckedBy)
        
        db.session.add(delivery)
        db.session.commit()

        return redirect(url_for('industrialist_inside_website' , user_id = user.user_id))
    
@app.route('/TransporterInsideWebsite/<user_id>' , methods = ['GET' , 'POST'])
def transporter_inside_website(user_id):
    if request.method == 'GET':
        return render_template('TransporterInsideWebsite.html' , user_id = user_id)
    elif request.method == 'POST':
        return render_template('TransporterInsideWebsite.html' , user_id = user_id)


@app.route('/ViewScheduledDeliveries' , methods = ['GET' , 'POST'])
def  view_scheduled_deliveries():
    my_table = []
    scheduled_deliveries = ScheduledDelivery.query.all()

    for delivery in scheduled_deliveries:
        if delivery.deal_done == False:
            industrialist = Industrialist.query.filter_by(user_id=delivery.user_id).first()
            user = User.query.filter_by(user_id=delivery.user_id).first()
            data = {
                'id': delivery.id,
                'pickup_location': delivery.pickup_location,
                'destination': delivery.destination,
                'proposed_amount': delivery.proposed_amount,
                'Vehicle_Type': delivery.vehicle_type,
                'Weight': delivery.weight,
                'Goods_Decription':delivery.Goods_Description
            }

            my_table.append(data)
    return render_template('ViewScheduledDeliveries.html' ,  my_table = my_table)
    

@app.route('/CustomerInsideWebsite/<user_id>' , methods = ['GET' , 'POST'])
def customer_inside_website(user_id):
    if request.method == 'GET':
        return render_template('CustomerInsideWebsite.html' , user_id = user_id)
    elif request.method == 'POST':
        return render_template('CustomerInsideWebsite.html' , user_id = user_id)

@app.route('/SignUp' , methods = ['GET' , 'POST'])
def signup_page():
    form = SignUpForm()
    if request.method == 'GET':
        return render_template('SignUpPage.html' , form = form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # user_name = form.username.data
            user_email = form.email.data
            existing_user = User.query.filter_by(email=user_email).first()
            if existing_user:
                return render_template('ErrorMessage.html', custom_error_message='Email already exists', heading='SIGN UP ERROR')
            password = form.password.data
            user_role = form.signup_as.data
            print(user_email)
            number = str(random_number_generator(6))
            msg = Message('6 DIGIT CODE', sender =   'hafizhashimkardar@gmail.com', body = 'HERE IS YOUR 6 DIGIT CODE.\n'+ number, recipients = [user_email])
            mail.send(msg)
            new_user = User(email = user_email, password = password , user_role=user_role)
            new_user_dict = {
                'user_id' : new_user.user_id,
                "email": new_user.email,
                "password" : new_user.password,
                "user_role" :  new_user.user_role,
            }
            session['data_to_send'] = new_user_dict
            session['number'] = int(number)
            return redirect(url_for('TakeRandomNumberInput'))
        else:
            if len(form.username.data) < 3 or len(form.username.data) > 20:
                return render_template('ErrorMessage.html' , custom_error_message = 'USERNAME LENGTH SHOULD BE AT LEAST 3 AND MAXIMUM 20' , heading = 'SIGN UP ERROR')
            elif len(form.password.data) < 6 or len(form.password.data) > 20:
                return render_template('ErrorMessage.html' , custom_error_message = 'PASSWORD LENGTH SHOULD BE AT LEAST 6 AND MAXIMUM 20' , heading = 'SIGN UP ERROR')

@app.route('/TakeRandomNumberInput' , methods = ['GET' , 'POST'])
def TakeRandomNumberInput():
    data = session['data_to_send']
    num  = session['number']
    if request.method == 'POST':
        input_num = int(request.form['input_num'])
        print(data)
        if num == input_num:
            if data['user_role'] == 'Customer':
                new_user = User(email = data['email'], password = data['password'] , user_role=data['user_role'])
                db.session.add(new_user)
                db.session.commit()
                recently_added_user = User.query.filter_by(email = data['email']).first()
                return redirect(url_for('CustomerSignUp', user_id = recently_added_user.user_id))
            elif data['user_role'] == 'Transporter':
                new_user = User(email = data['email'], password = data['password'] , user_role=data['user_role'])
                db.session.add(new_user)
                db.session.commit()
                recently_added_user = User.query.filter_by(email = data['email']).first()
                return redirect(url_for('TransporterSignUp' , user_id = recently_added_user.user_id))
            elif data['user_role'] == 'Industrialist':
                new_user = User(email = data['email'], password = data['password'] , user_role=data['user_role'])
                db.session.add(new_user)
                db.session.commit()
                recently_added_user = User.query.filter_by(email = data['email']).first()
                return redirect(url_for('IndustrialistSignUp' , user_id = recently_added_user.user_id))
            elif data['user_role'] == 'TruckDriver':
                new_user = User(email = data['email'], password = data['password'] , user_role=data['user_role'])
                db.session.add(new_user)
                db.session.commit()
                recently_added_user = User.query.filter_by(email = data['email']).first()
                return redirect(url_for('TruckDriverSignUp' , user_id = recently_added_user.user_id))
    elif request.method == 'GET':
        return render_template('RandomNumberInput.html')
        
@app.route('/Transporter')
def HomePage():
    return render_template('TransporterFeatures.html')

@app.route('/Mover')
def Mover():
    return render_template('HomePage2.html')

@app.route('/Driver')
def TruckDriver():
    return render_template('HomePage3.html')

@app.route('/TransporterSignUp/<user_id>' , methods = ['GET' , 'POST'])
def TransporterSignUp(user_id):
    form = TransporterSignUpForm()
    if request.method == 'GET':
        return render_template('TransporterSignUpCompletion.html' , user_id = user_id , form = form)
    elif request.method == 'POST':
        transporter_user_id = user_id
        transporter_name = form.transporter_name.data
        transporter_contact = form.contact_number.data
        transporter_address = form.address.data
        
        form.transporter_name = transporter_name
        form.contact_number = transporter_contact
        form.address = transporter_address

        print(form.data)

        if form.validate_on_submit():
            new_transporter = Transporter(user_id = transporter_user_id , transporter_name = transporter_name , contact_number = transporter_contact , address = transporter_address)
            db.session.add(new_transporter)
            db.session.commit()

            user_to_update = User.query.filter_by(user_id=transporter_user_id).first()
            if user_to_update:
                user_to_update.confirmed = True
            db.session.commit()

            return redirect(url_for('transporter_inside_website' , user_id = user_id))
        
        else:
            return render_template('HomePage1.html')

@app.route('/CustomerSignUp/<user_id>' , methods = ['GET' , 'POST'])
def CustomerSignUp(user_id):
    form = CustomerSignUpForm()
    if request.method == 'GET':
        return render_template('CustomerSignUpCompletion.html' , user_id = user_id , form = form)
    elif request.method == 'POST':
        customer_user_id = user_id
        customer_name = form.customer_name.data
        customer_contact = form.contact_number.data
        customer_address = form.address.data
        
        form.customer_name = customer_name
        form.contact_number =customer_contact
        form.address = customer_address

        print(form.data)
        if form.validate_on_submit():
            new_customer = Customer(user_id = customer_user_id , customer_name = customer_name , contact_number = customer_contact , address = customer_address)
            db.session.add(new_customer)
            db.session.commit()
            user_to_update = User.query.filter_by(user_id=customer_user_id).first()
            if user_to_update:
                user_to_update.confirmed = True
            db.session.commit()

            return redirect(url_for('customer_inside_website' , user_id = user_id))
        else:
            return render_template('HomePage2.html')
        



@app.route('/IndustrialistSignUp/<user_id>' , methods = ['GET' , 'POST'])
def IndustrialistSignUp(user_id):
    form = IndustrialistSignUpForm()
    if request.method == 'GET':
        return render_template('IndustrialistSignUpCompletion.html' , user_id = user_id , form = form)
    
    elif request.method == 'POST':
        industrialist_user_id = user_id
        industrialist_name = form.industrialist_name.data
        # industrialist_email = form.email.data
        industrialist_contact = form.contact_number.data
        industrialist_address = form.address.data

        form.industrialist_name = industrialist_name
        # form.email = industrialist_email
        form.contact_number =industrialist_contact
        form.address = industrialist_address

        if form.validate_on_submit():
            new_industrialist = Industrialist(user_id = user_id , industrialist_name = industrialist_name , contact_number = industrialist_contact , company_address = industrialist_address)
            db.session.add(new_industrialist)
            db.session.commit()
            user_to_update = User.query.filter_by(user_id=industrialist_user_id).first()
            if user_to_update:
                user_to_update.confirmed = True
            db.session.commit()
            return redirect(url_for('industrialist_inside_website' , user_id = user_id))
        
        else:
            return render_template('HomePage2.html')


@app.route('/TruckDriverSignUp/<user_id>' , methods = ['GET' , 'POST'])
def TruckDriverSignUp(user_id):
    form = DriverSignUpForm()
    if request.method == 'GET':
        return render_template('TruckDriverSignUpCompletion.html' , user_id = user_id , form = form)
    elif request.method == 'POST':
        driver_user_id = user_id
        driver_name = form.driver_name.data
        driver_license_number = form.license_number.data
        driver_contact_number = form.contact_number.data

        form.driver_name = driver_name
        form.license_number = driver_license_number
        form.contact_number = driver_contact_number

        if form.validate_on_submit():
            new_driver = Driver(user_id = driver_user_id , driver_name=driver_name , license_number=driver_license_number , contact_number=driver_contact_number)
            db.session.add(new_driver)
            db.session.commit()
            user_to_update = User.query.filter_by(user_id=driver_user_id).first()
            if user_to_update:
                user_to_update.confirmed = True
            db.session.commit()

        
        return render_template('MainHomePage.html')


@socketio.on('connect')
def handle_connect():
    user_type = request.args.get('user_type')
    if user_type == 'transporter':
        connected_transporters.append(request.sid)
    print(f'Client connected: {request.sid}, user type: {user_type}')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in connected_transporters:
        connected_transporters.remove(request.sid)
    print(f'Client disconnected: {request.sid}')



if __name__ == "__main__":
    socketio.run(app,debug=True)