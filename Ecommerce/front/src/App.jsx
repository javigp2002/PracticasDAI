import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Menu from './components/Menu.jsx'
import Resultados from './components/Resultados.jsx'
import { useEffect } from 'react'; // Add missing import statement
import { PrimeReactProvider, PrimeReactContext } from 'primereact/api';



function App() {
  const [productos, setProductos] = useState([])
  const [productosF, setProductosF] = useState([])

  const cambiado = (evento) => {
    console.log(typeof evento)
    if (typeof evento === "string") {
      console.log(evento)
      const filteredProductos = productos.filter((producto) => producto.category.includes(evento))
      setProductosF(filteredProductos)
    } else {
      if (evento.target.value !== "") {
        const filteredProductos = productos.filter((producto) => producto.category.includes(evento.target.value))
        setProductosF(filteredProductos)
      } else {
        setProductosF(productos)
      }
    }

   
   
  }

  useEffect(() => {
    fetch("http://localhost/api/productos?desde=0&hasta=100")
      .then((response) => response.json())
      .then((prods) => {
        setProductos(prods)
        setProductosF(prods)
      });
  }, [])

  return (
    <>
      <Menu cambiado={cambiado}/>
      <Resultados productos={productosF}/>
    </>
  )
}

export default App
