let allContainerCart = document.querySelector('.products');
let containerBuyCart = document.querySelector('.card-items');
let priceTotal = document.querySelector('.price-total')
let amountProduct = document.querySelector('.count-product');


let buyThings = [];
let totalCard = 0;
let countProduct = 0;

//functions
loadEventListeners();
function loadEventListeners() {
    allContainerCart.addEventListener('click', addProduct);
    containerBuyCart.addEventListener('click', deleteProduct);
    containerBuyCart.addEventListener('click', changeQuantity);
}

function addProduct(e){
    e.preventDefault();
    if (e.target.classList.contains('btn-add-cart')) {
        const selectProduct = e.target.parentElement;
        readTheContent(selectProduct);
    }
}

function deleteProduct(e) {
    if (e.target.classList.contains('delete-product')) {
        const deleteId = e.target.getAttribute('data-id');
        const deletedProduct = buyThings.find(product => product.id === deleteId);
        if (deletedProduct) {
            const priceReduce = parseFloat(deletedProduct.price) * parseFloat(deletedProduct.amount);
            totalCard -= priceReduce;
            totalCard = totalCard.toFixed(2);
            buyThings = buyThings.filter(product => product.id !== deleteId);
            countProduct--;
            loadHtml();
        }
    }

    if (buyThings.length === 0) {
        priceTotal.innerHTML = 0;
        amountProduct.innerHTML = 0;
    }
}

function readTheContent(product){
    const infoProduct = {
        image: product.querySelector('div img').src,
        title: product.querySelector('.title').textContent,
        price: parseFloat(product.querySelector('div p span').textContent),
        id: product.querySelector('a').getAttribute('data-id'),
        amount: 1
    }

    const existingProduct = buyThings.find(item => item.id === infoProduct.id);
    
    if (!existingProduct) {
        buyThings.push(infoProduct);
        totalCard += infoProduct.price;
        countProduct++;
        loadHtml();
    }
}

function loadHtml() {
    clearHtml();
    buyThings.forEach(product => {
        const { image, title, price, amount, id } = product;
        const row = document.createElement('div');
        row.classList.add('item');
        row.innerHTML = `
            <img src="${image}" alt="">
            <div class="item-content">
                <h5>${title}</h5>
                <h5 class="cart-price">${price}$</h5>
                <h6>Amount: <span class="amount">${amount}</span></h6>
                <div class="quantity-controls">
                    <button class="increase-amount" data-id="${id}">+</button>
                    <span class="product-quantity">${amount}</span>
                    <button class="decrease-amount" data-id="${id}">-</button>
                </div>
            </div>
            <span class="delete-product" data-id="${id}">X</span>
        `;
        containerBuyCart.appendChild(row);
    });

    let realizarPedidoBtn = document.getElementById('realizar-pedido-btn');
    if (!realizarPedidoBtn) {
        realizarPedidoBtn = document.createElement('button');
        realizarPedidoBtn.textContent = 'Realizar Pedido';
        realizarPedidoBtn.id = 'realizar-pedido-btn';
        containerBuyCart.appendChild(realizarPedidoBtn);
    }

    function handlePedidoConfirmado() {
        const confirmacion = confirm('¿Desea confirmar su pedido?');
        if (confirmacion) {
            buyThings = [];
            totalCard = 0;
            countProduct = 0;
            loadHtml();
            alert('¡Su pedido fue enviado!');
            realizarPedidoBtn.removeEventListener('click', handlePedidoConfirmado);
        }
    }

    realizarPedidoBtn.addEventListener('click', handlePedidoConfirmado);

    if (buyThings.length === 0) {
        realizarPedidoBtn.style.display = 'none';
    } else {
        realizarPedidoBtn.style.display = 'block';
    }

    priceTotal.innerHTML = totalCard;
    amountProduct.innerHTML = countProduct;
}


function changeQuantity(e) {
    if (e.target.classList.contains('increase-amount')) {
        const productId = e.target.getAttribute('data-id');
        const product = buyThings.find(item => item.id === productId);
        product.amount++;
        totalCard = parseFloat(totalCard) + parseFloat(product.price);
        totalCard = totalCard.toFixed(2);
        loadHtml();
    } else if (e.target.classList.contains('decrease-amount')) {
        const productId = e.target.getAttribute('data-id');
        const product = buyThings.find(item => item.id === productId);
        if (product.amount > 1) {
            product.amount--;
            totalCard = parseFloat(totalCard) - parseFloat(product.price);
            totalCard = totalCard.toFixed(2);
            loadHtml();
        }
    }
}

 function clearHtml(){
    containerBuyCart.innerHTML = '';
 }