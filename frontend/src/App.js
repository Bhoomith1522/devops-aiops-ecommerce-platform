import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [products, setProducts] = useState([]);

  const [name, setName] = useState("");

  const [price, setPrice] = useState("");

  // -----------------------------------
  // FETCH PRODUCTS
  // -----------------------------------

  const fetchProducts = async () => {

    try {

      const response = await axios.get(
        "http://localhost:5000/products"
      );

      setProducts(response.data);

    } catch (error) {

      console.error("Error fetching products:", error);
    }
  };

  // -----------------------------------
  // ADD PRODUCT
  // -----------------------------------

  const addProduct = async () => {

    if (!name || !price) {
      return;
    }

    try {

      await axios.post(
        "http://localhost:5000/products",
        {
          name: name,
          price: parseInt(price)
        }
      );

      setName("");
      setPrice("");

      fetchProducts();

    } catch (error) {

      console.error("Error adding product:", error);
    }
  };

  // -----------------------------------
  // DELETE PRODUCT
  // -----------------------------------

  const deleteProduct = async (id) => {

    try {

      await axios.delete(
        `http://localhost:5000/products/${id}`
      );

      fetchProducts();

    } catch (error) {

      console.error("Error deleting product:", error);
    }
  };

  // -----------------------------------
  // LOAD PRODUCTS
  // -----------------------------------

  useEffect(() => {

    fetchProducts();

  }, []);

  // -----------------------------------
  // UI
  // -----------------------------------

  return (

    <div style={{ padding: "30px" }}>

      <h1>DevOps + AIOps E-Commerce</h1>

      <h2>Add Product</h2>

      <input
        type="text"
        placeholder="Product Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />

      <button onClick={addProduct}>
        Add Product
      </button>

      <hr />

      <h2>Products</h2>

      {products.map((product) => (

        <div
          key={product.id}
          style={{
            border: "1px solid gray",
            padding: "10px",
            marginBottom: "10px"
          }}
        >

          <h3>{product.name}</h3>

          <p>₹ {product.price}</p>

          <button
            onClick={() => deleteProduct(product.id)}
          >
            Delete
          </button>

        </div>
      ))}

    </div>
  );
}

export default App;