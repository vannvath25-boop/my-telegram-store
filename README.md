<!DOCTYPE html>
<html lang="km" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Telegram Store Mini App</title>
    <!-- Telegram WebApp SDK -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts Khmer -->
    <link href="https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0f9ff',
                            500: '#0088cc',
                            600: '#0077b3',
                            700: '#005580',
                        },
                        acleda: '#003B71'
                    },
                    fontFamily: {
                        khmer: ['Kantumruy Pro', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Kantumruy Pro', sans-serif;
            -webkit-tap-highlight-color: transparent;
            user-select: none;
        }
        .hide-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .hide-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen pb-24 font-khmer antialiased">

    <!-- TOP BAR / HEADER -->
    <header class="sticky top-0 z-30 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 px-4 py-3">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="relative">
                    <img id="user-avatar" class="w-10 h-10 rounded-full border-2 border-brand-500 object-cover" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80" alt="Avatar">
                    <span class="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 border-2 border-slate-900 rounded-full"></span>
                </div>
                <div>
                    <h2 id="user-name" class="font-bold text-sm text-slate-100 flex items-center gap-1">
                        រង់ចាំការទាញយក... 
                    </h2>
                    <p id="user-id" class="text-xs text-slate-400">ID: --</p>
                </div>
            </div>
            
            <!-- Cart Button with Badge -->
            <button onclick="toggleCartModal(true)" class="relative bg-slate-800 hover:bg-slate-700 p-2.5 rounded-xl border border-slate-700 text-slate-200 transition-all active:scale-95">
                <i class="fa-solid fa-cart-shopping text-lg text-brand-500"></i>
                <span id="cart-badge" class="hidden absolute -top-1.5 -right-1.5 bg-rose-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full animate-bounce">0</span>
            </button>
        </div>

        <!-- Search Bar -->
        <div class="mt-3 relative">
            <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
            <input type="text" id="search-input" oninput="filterProducts()" placeholder="ស្វែងរកអីវ៉ាន់..." class="w-full bg-slate-800/90 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-brand-500 transition-colors">
        </div>
    </header>

    <!-- CATEGORIES SCROLL -->
    <div class="px-4 py-3 border-b border-slate-800/60 overflow-x-auto hide-scrollbar">
        <div class="flex space-x-2" id="category-container">
            <!-- Rendered by JS -->
        </div>
    </div>

    <!-- MAIN PRODUCT GRID -->
    <main class="p-4">
        <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-200 text-base flex items-center gap-2">
                <i class="fa-solid fa-fire text-amber-500"></i> ទំនិញទាំងអស់
            </h3>
            <span id="product-count" class="text-xs text-slate-400">0 មុខ</span>
        </div>
        
        <div class="grid grid-cols-2 gap-3.5" id="products-grid">
            <!-- Rendered by JS -->
        </div>
    </main>

    <!-- BOTTOM CART BAR (FLOATING WHEN CART NOT EMPTY) -->
    <div id="floating-cart-bar" class="hidden fixed bottom-4 left-4 right-4 z-20">
        <div class="bg-gradient-to-r from-brand-600 to-blue-600 rounded-2xl p-3.5 shadow-xl shadow-brand-500/20 flex items-center justify-between border border-brand-500/40">
            <div class="flex items-center space-x-3">
                <div class="bg-white/20 p-2.5 rounded-xl text-white">
                    <i class="fa-solid fa-basket-shopping text-xl"></i>
                </div>
                <div>
                    <p class="text-xs text-blue-100">សរុបក្នុងកន្ត្រក (<span id="float-cart-count">0</span>)</p>
                    <p class="text-lg font-bold text-white" id="float-cart-total">$0.00</p>
                </div>
            </div>
            <button onclick="toggleCartModal(true)" class="bg-white text-brand-700 font-bold px-4 py-2.5 rounded-xl text-sm hover:bg-slate-100 active:scale-95 transition-all shadow-md">
                ពិនិត្យមើល <i class="fa-solid fa-arrow-right ml-1"></i>
            </button>
        </div>
    </div>

    <!-- CART MODAL -->
    <div id="cart-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex justify-end flex-col transition-opacity duration-300">
        <div class="bg-slate-900 border-t border-slate-700 rounded-t-3xl max-h-[85vh] flex flex-col overflow-hidden">
            <!-- Modal Header -->
            <div class="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
                <h3 class="font-bold text-lg text-slate-100 flex items-center gap-2">
                    <i class="fa-solid fa-cart-shopping text-brand-500"></i> កន្ត្រកទំនិញ
                </h3>
                <button onclick="toggleCartModal(false)" class="w-8 h-8 rounded-full bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <!-- Modal Body (Cart Items) -->
            <div id="cart-items-list" class="p-4 overflow-y-auto space-y-3 flex-1">
                <!-- Items populated by JS -->
            </div>

            <!-- Modal Footer -->
            <div class="p-4 border-t border-slate-800 bg-slate-950 space-y-3">
                <div class="space-y-1.5 text-sm">
                    <div class="flex justify-between text-slate-400">
                        <span>តម្លៃសរុប (Subtotal):</span>
                        <span id="cart-subtotal">$0.00</span>
                    </div>
                    <div class="flex justify-between text-slate-400">
                        <span>សេវាដឹក/បញ្ជូន:</span>
                        <span class="text-emerald-400">ឥតគិតថ្លៃ</span>
                    </div>
                    <div class="flex justify-between text-base font-bold text-slate-100 pt-2 border-t border-slate-800">
                        <span>ទឹកប្រាក់ត្រូវទូទាត់:</span>
                        <span class="text-brand-500 text-lg" id="cart-final-total">$0.00</span>
                    </div>
                </div>

                <button onclick="openPaymentModal()" class="w-full bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-white font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-600/20 flex items-center justify-center gap-2 transition-all">
                    <i class="fa-solid fa-qrcode text-lg"></i> បន្តទៅទូទាត់ប្រាក់ (ACLEDA KHQR)
                </button>
            </div>
        </div>
    </div>

    <!-- PAYMENT MODAL (ACLEDA / KHQR) -->
    <div id="payment-modal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
            <!-- Header -->
            <div class="bg-acleda px-4 py-3 flex items-center justify-between text-white">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-building-columns text-amber-400 text-lg"></i>
                    <span class="font-bold text-sm tracking-wide">ACLEDA / KHQR PAYMENT</span>
                </div>
                <button onclick="togglePaymentModal(false)" class="text-slate-300 hover:text-white">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <!-- Payment Content -->
            <div class="p-5 overflow-y-auto space-y-4 text-center">
                <div>
                    <p class="text-xs text-slate-400">ចំនួនទឹកប្រាក់ត្រូវ Scan បាញ់:</p>
                    <h2 class="text-2xl font-black text-amber-400 mt-0.5" id="pay-amount">$0.00</h2>
                    <p class="text-[11px] text-slate-500">គណនី: <span class="text-slate-300 font-semibold">VATH STORE</span></p>
                </div>

                <!-- QR CODE DISPLAY -->
                <div class="bg-white p-3.5 rounded-2xl inline-block shadow-inner border-2 border-amber-400/50 relative">
                    <img id="qr-image" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=ACLEDA_KHQR_VATH_STORE" alt="ACLEDA KHQR" class="w-48 h-48 mx-auto object-contain">
                    <div class="mt-2 pt-2 border-t border-slate-200 flex items-center justify-center gap-1 text-[11px] font-bold text-slate-800">
                        <span class="text-red-600">KHQR</span> | ACLEDA Bank
                    </div>
                </div>

                <p class="text-xs text-slate-300">សូម Scan QR ខាងលើតាមកម្មវិធី **ACLEDA Mobile** ឬធនាគារផ្សេងៗ</p>

                <!-- UPLOAD RECEIPT SECTION -->
                <div class="text-left bg-slate-800/80 p-3 rounded-xl border border-slate-700/80">
                    <label class="block text-xs font-semibold text-slate-300 mb-1.5">
                        <i class="fa-solid fa-receipt text-brand-500"></i> ភ្ជាប់រូបថតវិក្កយបត្រ/ប័ណ្ណទូទាត់ (Receipt):
                    </label>
                    <input type="file" id="receipt-file" accept="image/*" class="text-xs text-slate-400 file:mr-2 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-brand-600 file:text-white hover:file:bg-brand-500 cursor-pointer w-full">
                </div>
            </div>

            <!-- Footer Action -->
            <div class="p-4 bg-slate-950 border-t border-slate-800">
                <button onclick="submitOrder()" class="w-full bg-brand-600 hover:bg-brand-500 active:scale-[0.98] text-white font-bold py-3 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2">
                    <i class="fa-paper-plane"></i> ផ្ញើប័ណ្ណទូទាត់ទៅ Admin
                </button>
            </div>
        </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div id="toast" class="fixed top-5 left-1/2 -translate-x-1/2 z-50 bg-slate-800 border border-slate-700 text-slate-100 px-4 py-2.5 rounded-2xl shadow-xl text-xs font-medium flex items-center space-x-2 transition-all duration-300 opacity-0 pointer-events-none">
        <i id="toast-icon" class="fa-solid fa-circle-check text-emerald-400 text-sm"></i>
        <span id="toast-message">សារជូនដំណឹង</span>
    </div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        // TELEGRAM SDK INITIALIZATION
        const tg = window.Telegram?.WebApp;
        if (tg) {
            tg.ready();
            tg.expand();
            tg.enableClosingConfirmation();
        }

        // SAMPLE PRODUCTS DATA
        const products = [
            { id: 1, name: "Mobile Legends 1000 Diamonds", category: "Gaming", price: 14.50, image: "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=300&q=80", tag: "Hot" },
            { id: 2, name: "PUBG Mobile 660 UC", category: "Gaming", price: 9.99, image: "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=300&q=80", tag: "Popular" },
            { id: 3, name: "Netflix Premium 1 ខែ", category: "Accounts", price: 3.50, image: "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?auto=format&fit=crop&w=300&q=80", tag: "Best Seller" },
            { id: 4, name: "Spotify Premium 1 ឆ្នាំ", category: "Accounts", price: 12.00, image: "https://images.unsplash.com/photo-1614680376593-902f749f704b?auto=format&fit=crop&w=300&q=80", tag: "Sale" },
            { id: 5, name: "Telegram Premium 1 ឆ្នាំ", category: "Services", price: 28.00, image: "https://images.unsplash.com/photo-1611729643739-4c2237016335?auto=format&fit=crop&w=300&q=80", tag: "New" },
            { id: 6, name: "Canva Pro 1 ឆ្នាំ (Edu)", category: "Services", price: 4.99, image: "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=300&q=80", tag: "Discount" }
        ];

        const categories = ["ទាំងអស់", "Gaming", "Accounts", "Services"];
        let currentCategory = "ទាំងអស់";
        let cart = [];

        // INIT APP
        document.addEventListener("DOMContentLoaded", () => {
            loadUserProfile();
            renderCategories();
            renderProducts(products);
        });

        // USER PROFILE FROM TELEGRAM
        function loadUserProfile() {
            if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
                const user = tg.initDataUnsafe.user;
                document.getElementById('user-name').innerText = `${user.first_name} ${user.last_name || ''}`;
                document.getElementById('user-id').innerText = `ID: ${user.id}`;
                if (user.photo_url) {
                    document.getElementById('user-avatar').src = user.photo_url;
                }
            } else {
                document.getElementById('user-name').innerText = "Vath Guest";
                document.getElementById('user-id').innerText = "ID: 987654321";
            }
        }

        // RENDER CATEGORIES
        function renderCategories() {
            const container = document.getElementById('category-container');
            container.innerHTML = categories.map(cat => `
                <button onclick="selectCategory('${cat}')" class="px-4 py-1.5 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${currentCategory === cat ? 'bg-brand-600 text-white shadow-md shadow-brand-600/30' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}">
                    ${cat}
                </button>
            `).join('');
        }

        function selectCategory(cat) {
            triggerHaptic();
            currentCategory = cat;
            renderCategories();
            filterProducts();
        }

        // FILTER & RENDER PRODUCTS
        function filterProducts() {
            const query = document.getElementById('search-input').value.toLowerCase();
            const filtered = products.filter(p => {
                const matchCat = currentCategory === "ទាំងអស់" || p.category === currentCategory;
                const matchSearch = p.name.toLowerCase().includes(query);
                return matchCat && matchSearch;
            });
            renderProducts(filtered);
        }

        function renderProducts(list) {
            const grid = document.getElementById('products-grid');
            document.getElementById('product-count').innerText = `${list.length} មុខ`;

            if(list.length === 0) {
                grid.innerHTML = `<div class="col-span-2 text-center py-10 text-slate-500 text-sm">រកមិនឃើញទំនិញឡើយ!</div>`;
                return;
            }

            grid.innerHTML = list.map(p => `
                <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl overflow-hidden flex flex-col justify-between hover:border-slate-600 transition-all">
                    <div class="relative">
                        <img src="${p.image}" alt="${p.name}" class="w-full h-28 object-cover">
                        <span class="absolute top-2 left-2 bg-slate-900/80 backdrop-blur-md text-amber-400 text-[10px] font-bold px-2 py-0.5 rounded-md border border-slate-700">
                            ${p.tag}
                        </span>
                    </div>
                    <div class="p-3 flex-1 flex flex-col justify-between">
                        <div>
                            <p class="text-[10px] text-brand-500 font-semibold uppercase tracking-wider">${p.category}</p>
                            <h4 class="font-semibold text-xs text-slate-100 leading-snug line-clamp-2 mt-0.5">${p.name}</h4>
                        </div>
                        <div class="mt-3 flex items-center justify-between">
                            <span class="text-sm font-bold text-emerald-400">$${p.price.toFixed(2)}</span>
                            <button onclick="addToCart(${p.id})" class="bg-brand-600 hover:bg-brand-500 active:scale-90 text-white w-7 h-7 rounded-lg flex items-center justify-center transition-all shadow-md">
                                <i class="fa-solid fa-plus text-xs"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // CART LOGIC
        function addToCart(productId) {
            triggerHaptic();
            const product = products.find(p => p.id === productId);
            const existing = cart.find(item => item.id === productId);

            if (existing) {
                existing.qty++;
            } else {
                cart.push({ ...product, qty: 1 });
            }

            updateCartUI();
            showToast(`បានបន្ថែម "${product.name}" ទៅក្នុងកន្ត្រក`);
        }

        function updateCartQty(id, change) {
            triggerHaptic();
            const item = cart.find(i => i.id === id);
            if (item) {
                item.qty += change;
                if (item.qty <= 0) {
                    cart = cart.filter(i => i.id !== id);
                }
            }
            updateCartUI();
            renderCartModalItems();
        }

        function updateCartUI() {
            const totalQty = cart.reduce((sum, item) => sum + item.qty, 0);
            const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);

            // Badge
            const badge = document.getElementById('cart-badge');
            if (totalQty > 0) {
                badge.innerText = totalQty;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }

            // Floating Bar
            const floatBar = document.getElementById('floating-cart-bar');
            if (totalQty > 0) {
                floatBar.classList.remove('hidden');
                document.getElementById('float-cart-count').innerText = totalQty;
                document.getElementById('float-cart-total').innerText = `$${totalPrice.toFixed(2)}`;
            } else {
                floatBar.classList.add('hidden');
            }

            // Totals in Modal
            document.getElementById('cart-subtotal').innerText = `$${totalPrice.toFixed(2)}`;
            document.getElementById('cart-final-total').innerText = `$${totalPrice.toFixed(2)}`;
            document.getElementById('pay-amount').innerText = `$${totalPrice.toFixed(2)}`;
        }

        function toggleCartModal(show) {
            triggerHaptic();
            const modal = document.getElementById('cart-modal');
            if (show) {
                renderCartModalItems();
                modal.classList.remove('hidden');
            } else {
                modal.classList.add('hidden');
            }
        }

        function renderCartModalItems() {
            const container = document.getElementById('cart-items-list');
            if (cart.length === 0) {
                container.innerHTML = `<div class="text-center py-12 text-slate-500 text-sm">មិនទាន់មានអីវ៉ាន់ក្នុងកន្ត្រកនៅឡើយទេ</div>`;
                return;
            }

            container.innerHTML = cart.map(item => `
                <div class="flex items-center justify-between bg-slate-800/80 p-2.5 rounded-xl border border-slate-700/60">
                    <div class="flex items-center space-x-3">
                        <img src="${item.image}" class="w-12 h-12 rounded-lg object-cover">
                        <div>
                            <h4 class="text-xs font-semibold text-slate-100">${item.name}</h4>
                            <p class="text-xs text-emerald-400 font-bold">$${(item.price * item.qty).toFixed(2)}</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2 bg-slate-900 px-2 py-1 rounded-lg border border-slate-700">
                        <button onclick="updateCartQty(${item.id}, -1)" class="text-slate-400 hover:text-white px-1">-</button>
                        <span class="text-xs font-bold text-slate-100 w-4 text-center">${item.qty}</span>
                        <button onclick="updateCartQty(${item.id}, 1)" class="text-slate-400 hover:text-white px-1">+</button>
                    </div>
                </div>
            `).join('');
        }

        // PAYMENT MODAL
        function openPaymentModal() {
            if (cart.length === 0) {
                showToast("សូមជ្រើសរើសទំនិញយ៉ាងហោច 1 មុននឹងទូទាត់");
                return;
            }
            toggleCartModal(false);
            togglePaymentModal(true);
        }

        function togglePaymentModal(show) {
            triggerHaptic();
            const modal = document.getElementById('payment-modal');
            if (show) {
                modal.classList.remove('hidden');
            } else {
                modal.classList.add('hidden');
            }
        }

        // SUBMIT ORDER TO ADMIN
        function submitOrder() {
            triggerHaptic();
            const receiptInput = document.getElementById('receipt-file');
            
            if (receiptInput.files.length === 0) {
                showToast("សូម Attach/Upload រូបថតវិក្កយបត្រទូទាត់ជាមុនសិន!");
                return;
            }

            showToast("កុំពុងផ្ញើព័ត៌មាន Order...");

            setTimeout(() => {
                togglePaymentModal(false);
                cart = [];
                updateCartUI();
                showToast("ការបញ្ជាទិញជោគជ័យ! Admin នឹងពិនិត្យឆាប់ៗនេះ។");
                
                // Telegram MainButton Feedback
                if (tg) {
                    tg.showAlert("អរគុណសម្រាប់ការបញ្ជាទិញ! ព័ត៌មាន Order ត្រូវបានផ្ញើទៅ Admin រួចរាល់ហើយ។");
                }
            }, 1200);
        }

        // HELPERS
        function showToast(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-message').innerText = msg;
            toast.classList.remove('opacity-0', 'pointer-events-none');
            setTimeout(() => {
                toast.classList.add('opacity-0', 'pointer-events-none');
            }, 2500);
        }

        function triggerHaptic() {
            if (tg && tg.HapticFeedback) {
                tg.HapticFeedback.impactOccurred('medium');
            }
        }
    </script>
</body>
</html> 
