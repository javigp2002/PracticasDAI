// se ejecuta recien cargada la página

document.addEventListener('DOMContentLoaded', () => {
	// donde se inyecte el código html
	const span_para_estrellas = document.querySelectorAll('span.sp') 

	span_para_estrellas.forEach((ele) => {   // arrow function
		// comillas hacia atrás: es6 multiline
		// conectar con el api para recoger el rating y ponerlo
		// busca el resultado según el id de cada elemento y encuentra el rating de cada uno
		
		fetch(`http://localhost:8000/api/productos/${ele.id}`)
			.then(response => response.json())
			.then(data => {
				const rating = data.rating;
				const rate = data.rate;
				
				if (rating >= 2.5){
					ele.innerHTML = `                                        
						<span class="fa fa-star not_checked"></span>
						<span class="fa fa-star not_checked"></span>
						<span class="fa fa-star not_checked"></span>
						<span class="fa fa-star not_checked"></span>
						<span class="fa fa-star not_checked"></span>
					`
				}else{
					ele.innerHTML = `                                        
						<span class="fa fa-star checked"></span>
						<span class="fa fa-star checked"></span>
						<span class="fa fa-star checked"></span>
						<span class="fa fa-star checked"></span>
						<span class="fa fa-star checked"></span>
					`
				}


			})
	})
})