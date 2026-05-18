import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [logText, setLogText] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);

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

      console.error(error);
    }
  };

  useEffect(() => {

    fetchProducts();

  }, []);

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
          name,
          price
        }
      );

      setName("");
      setPrice("");

      fetchProducts();

    } catch (error) {

      console.error(error);
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

      console.error(error);
    }
  };

  // -----------------------------------
  // ANALYZE LOG
  // -----------------------------------

  const analyzeLog = async () => {

    if (!logText) {
      return;
    }

    try {

      setLoading(true);

      const response = await axios.post(
        "http://localhost:5000/analyze-log",
        {
          log: logText
        }
      );

      setAnalysis(response.data.analysis);

      setLoading(false);

    } catch (error) {

      console.error(error);

      setLoading(false);
    }
  };

  return (

    <div className="app-container">

      <div className="overlay"></div>

      <div className="content">

        {/* HEADER */}

        <div className="header-card">

          <h1>
            DevOps + AIOps Monitoring Platform
          </h1>

          <p>
            AI-Powered Full Stack Monitoring Dashboard
          </p>

        </div>

        {/* STATS */}

        <div className="stats-grid">

          <div className="stat-card">
            <h2>{products.length}</h2>
            <span>Total Products</span>
          </div>

          <div className="stat-card">
            <h2>Docker</h2>
            <span>Containerized Infrastructure</span>
          </div>

          <div className="stat-card">
            <h2>AI Ops</h2>
            <span>Log Intelligence Enabled</span>
          </div>

        </div>

        {/* PRODUCT SECTION */}

        <div className="section-card">

          <h2>Add Product</h2>

          <div className="form-row">

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

          </div>

        </div>

        {/* PRODUCTS LIST */}

        <div className="section-card">

          <h2>Products</h2>

          <div className="products-grid">

            {products.map((product) => (

              <div
                className="product-card"
                key={product.id}
              >

                <h3>{product.name}</h3>

                <p>₹ {product.price}</p>

                <button
                  className="delete-btn"
                  onClick={() => deleteProduct(product.id)}
                >
                  Delete
                </button>

              </div>
            ))}

          </div>

        </div>

        {/* AIOPS */}

        <div className="section-card">

          <h2>AIOps Log Analysis</h2>

          <textarea
            placeholder="Paste DevOps logs here..."
            value={logText}
            onChange={(e) => setLogText(e.target.value)}
          ></textarea>

          <button
            className="analyze-btn"
            onClick={analyzeLog}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Logs"}
          </button>

          {
            analysis && (

              <div className="analysis-box">

                <h3>AI Analysis</h3>

                <pre>{analysis}</pre>

              </div>
            )
          }

        </div>

      </div>

    </div>
  );
}

export default App;