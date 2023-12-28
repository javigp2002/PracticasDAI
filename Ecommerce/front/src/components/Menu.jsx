// Para crearlo rapido "rfc"
import React from 'react'
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';



export default function Menu({cambiado}) {
    return (
        <Navbar expand="lg" className="bg-body-tertiary" fixed="top">
        <Container fluid>
            <Navbar.Brand href="#">Tienda Dai </Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
                <Nav
                    className="me-auto my-2 my-lg-0"
                    style={{ maxHeight: '100px' }}
                    navbarScroll
                >
                    <Nav.Link href="#action1">Tienda DAI</Nav.Link>
                    <NavDropdown title="Categorias" id="navbarScrollingDropdown">
                        <NavDropdown.Item onClick={() => cambiado("electronics")}>Electronics</NavDropdown.Item>
                        <NavDropdown.Item onClick={() => cambiado("jewelery")}>Jewelry</NavDropdown.Item>
                        <NavDropdown.Item onClick={() => cambiado("men's clothing")}>Men's fashion</NavDropdown.Item>
                        <NavDropdown.Item onClick={() => cambiado("women's clothing")}>Women's fashion</NavDropdown.Item>

                        <NavDropdown.Divider />
                        <NavDropdown.Item href="#action5">
                            All products
                        </NavDropdown.Item>
                    </NavDropdown>
                </Nav>
                <Form className="d-flex">
                    <Form.Control
                        type="search"
                        placeholder="Search"
                        className="me-2"
                        aria-label="Search"
                        onChange={ (evento) => {cambiado(evento)}}
                    />
                    <Button variant="outline-success">Search</Button>
                </Form>
            </Navbar.Collapse>
        </Container>
    </Navbar>
                
        )
}
