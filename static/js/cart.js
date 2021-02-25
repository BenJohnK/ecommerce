var updateBtns = document.getElementsByClassName('update-cart');

for (i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){

        var productId = this.dataset.product
        var action= this.dataset.action
        console.log("productId: ",productId,"Action: ",action)

        console.log('User: ',user)
        if(user === "AnonymousUser"){
            addItems(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}
function updateUserOrder(productid,action){
    console.log("User is logged in. Sending data..")

    var url='/store/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productid':productid,'action':action})

    })

    .then((response)=>{
        return response.json()
    })
    
    .then((data)=>{
        console.log('data: ',data)
        location.reload()
    })
    
}
function addItems(productid,action){
    console.log("creating cart for anonymous user")
    if(action=="add"){
        if(cart[productid]==undefined){
            cart[productid]={'quantity':1} 
        }else{
            cart[productid]['quantity']+=1
        }
    }
    if(action=="remove"){
        cart[productid]['quantity']-=1
        if(cart[productid]['quantity']<=0){
            delete cart[productid]
        }
    }
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
    console.log('cart: ',cart)
    location.reload()
}