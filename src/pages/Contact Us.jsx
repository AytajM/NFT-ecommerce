import React, { useState } from "react";
import {Link, useNavigate} from "react-router-dom";
//import axios from 'axios'



const ContactUs = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };
const navigate = useNavigate()

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("http://localhost:8000/nfts/send-email/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        message: message,
      }),
    })
      .then((response) => response.json)
      .then((data) => navigate("/messagesent"))
      .catch((error)=>console.log(error))

    // Reset form
    setName("");
    setEmail("");
    setMessage("");
  };

  return (
    <>
      <div id="stars"></div>
      <div id="stars2"></div>
      <div id="stars3"></div>

      <div className="container contact_us_container">
        <div>
          <div className="mb-5 mt-3">
            <h1 className="display-4 mb-4">Contact Us</h1>
          </div>
          <br />
          <div className="sec_sp">
            <div className="mb-5">
              <h3 className="color_sec py-4">Get In Touch</h3>
              <address>
                <strong>Email: nftwebsite23@outlook.com</strong>
                <br />
                <br />
                <p>
                  <strong>Phone: +994 50 999 99 99</strong>
                </p>
              </address>
            </div>
            <div className="d-flex align-items-center">
              <form
                className="contact__form"
                action="contact/"
                method="POST"
                onSubmit={handleSubmit}
              >
                <div className="row">
                  <div className="col-lg-6 form-group">
                    <input
                      className="input_css"
                      id="name"
                      name="name"
                      placeholder="Name"
                      type="text"
                      value={name}
                      onChange={handleNameChange}
                    />
                  </div>
                  <div className="col-lg-6 form-group">
                    <input
                      className="input_css rounded-0"
                      id="email"
                      name="email"
                      placeholder="Email"
                      type="email"
                      value={email}
                      onChange={handleEmailChange}
                    />
                  </div>
                </div>
                <textarea
                  className="input_css rounded-0"
                  id="message"
                  name="message"
                  placeholder="Message"
                  rows="5"
                  value={message}
                  onChange={handleMessageChange}
                ></textarea>
                <br />
                <div className="row">
                  <div className="col-lg-12 form-group">
                    
                    <button className="btn contact_btn" type="submit">
                      Send
                    </button>
                    
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ContactUs;
