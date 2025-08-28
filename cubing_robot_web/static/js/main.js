'use strict';

(function(){
	const flashes = document.querySelectorAll('.flash');
	flashes.forEach(el => {
		setTimeout(() => {
			el.style.transition = 'opacity .3s ease, transform .3s ease';
			el.style.opacity = '0';
			el.style.transform = 'translateY(-4px)';
			setTimeout(()=> el.remove(), 350);
		}, 3000);
	});
})();
