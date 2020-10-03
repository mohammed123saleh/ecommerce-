class Item(models.Model):
    title = models.CharField(max_length=250, unique=False)
    Company = models.CharField(max_length=260, unique=False, null=True, blank=True)
    price = models.FloatField(unique=False)
    highest_price = models.FloatField(unique=False, default=1000) 
    discount_price = models.FloatField(blank=True, null=True, editable=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2,blank=True, null=True, editable=False)
    description = models.TextField() 
    slug = models.SlugField(max_length=300, unique=False,help_text='random input')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='Egypt_fabrics', blank=False, null=False )



    def __str__(self):
        return self.title
    def save(self, *args, **kwargs, ):

        self.slug = slugify(self.title + self.slug + str(self.price) + '/' )+ mar
        super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Main:product", kwargs={
        'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("Main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("Main:remove-from-cart", kwargs={
            'slug': self.slug
        })



'''

i add the var_category tuple and Variation model recently after
the customer asked me to add variation but:

1- Item model
2- OrderItem model 
3- Order model 

these three were in the working website

'''
var_category = (
    ('size','size'),
   
)
  
class Variation(models.Model):
    itemy = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=var_category, default='size')
    price_var = models.FloatField(null=True, blank=True)




    def __str__(self):
        return self.title + ' ' + self.item.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation)
    quantity = models.IntegerField(default=1)
    

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

  
    def get_total_item_price(self):
       

   
        return self.quantity *  self.item.price   # here i should to insert the duration  which will come from the form  datepicker which comes from django-bootstrap-datepicker

    def get_total_discount_item_price(self):
                
        
        return self.quantity *  self.item.price   # here i should to insert the duration  which will come from the form  datepicker which comes from django-bootstrap-datepicker

    def get_amount_saved(self):
        return self.get_total_item_price() - 0

    def get_final_price(self):

        return self.get_total_item_price()




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
       'Address', on_delete=models.SET_NULL, blank=True, null=True)
   
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

