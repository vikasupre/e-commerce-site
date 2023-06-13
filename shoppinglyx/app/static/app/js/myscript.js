$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr('pid').toString()
    let elm = (this.parentNode.children[2])
    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: { prod_id: id },
        success: function (mydata) {
            elm.innerText = mydata.quantity
            document.getElementById('amount').innerText = mydata.amount
            document.getElementById('totalamount').innerText = mydata.total_amount
        }
    })

})

$('.minus-cart').click(function(){
    let id=$(this).attr('pid').toString()
    let elm=this.parentNode.children[2]

    $.ajax({
        type:'GET',
        url:'/minuscart',
        data:{prod_id:id},
        success:function(mydata){
            elm.innerText=mydata.quantity
            document.getElementById('amount').innerText = mydata.amount
            document.getElementById('totalamount').innerText = mydata.totalamount
        }
    })
})

$('.remove').click(function(){
    let id=$(this).attr('pid').toString()
    let elm=this.parentNode.parentNode.parentNode.parentNode

    $.ajax({
        type:'GET',
        url:'/removeitem',
        data:{prod_id:id},
        success:function(mydata){
            elm.remove()
            document.getElementById('amount').innerText = mydata.amount
            document.getElementById('totalamount').innerText = mydata.totalamount


        }
    })
})