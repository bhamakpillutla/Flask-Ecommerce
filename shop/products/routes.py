from flask import redirect,current_app, render_template, url_for, flash, request, session
from shop import db, app, photos
from .models import Brand,Category,Addproduct
from .forms import Addproducts

import secrets,os

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    ## picks only available/existing product brands and categories
    brands = Brand.query.join(Addproduct, ( Brand.id== Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', products=products, brands= brands, categories=categories)


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, ( Brand.id== Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/single_page.html', product=product, brands=brands, categories=categories)



@app.route('/brand/<int:id>')
def get_brand(id):
    ## pagination
    page = request.args.get('page', 1, type=int)
    ## for pagination id
    getbrand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=getbrand).paginate(page=page, per_page=6)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    ## to display categories in brands dropdown menu
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brand= brand,brands=brands, categories=categories, getbrand=getbrand)

@app.route('/categories/<int:id>')
def get_category(id):
    ## pagination
    page = request.args.get('page', 1, type=int)
    ## for pagination id
    getcat = Category.query.filter_by(id=id).first_or_404()
    get_cat = Addproduct.query.filter_by(category= getcat).paginate(page=page, per_page=6)
    ##  to display brands in categories dropdown menu
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', get_cat= get_cat ,brands=brands, categories=categories, getcat=getcat)

# add brand
@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to you database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    # brand = updatebrand.name
    return render_template('products/updatebrand.html', title='Update brand',updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


# add category
@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to you database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('category'))
    # category = updatecat.name
    return render_template('products/updatebrand.html', title='Update cat',updatecat=updatecat)



@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 =photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 =photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        image_3 =photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        addpro = Addproduct(name=name, price=price, discount= discount, stock=stock, colors=colors, desc=desc, brand_id= brand, category_id=category,image_1= image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title = 'Add Product page', form=form, brands = brands, categories= categories)

# update product
@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method=='POST':
        # update information
        product.name= form.name.data
        product.price = form.price.data
        product.discount=form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.desc = form.description.data
        # update images
        if request.files.get('image_1'):
            try:
                # first removes image from the folder
                os.unlink(os.path.join(current_app.root_path,'static/images/'+product.image_1))
                # uploads new image
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        if request.files.get('image_2'):
            try:
                # first removes image from the folder
                os.unlink(os.path.join(current_app.root_path,'static/images/'+product.image_2))
                # uploads new image
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        if request.files.get('image_3'):
            try:
                # first removes image from the folder
                os.unlink(os.path.join(current_app.root_path,'static/images/'+product.image_3))
                # uploads new image
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        db.session.commit()
        flash(f'Your product {product.name} has been updated ', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc

    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product= product)



@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete the product','success')
    return redirect(url_for('admin'))