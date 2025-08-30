import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>Product</h4>
          <ul>
            <li><a href="#how-it-works">How it works</a></li>
            <li><a href="#">Pricing</a></li>
            <li><a href="#">Security</a></li>
            <li><a href="#">Changelog</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>Company</h4>
          <ul>
            <li><a href="#">About</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>Legal</h4>
          <ul>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">DPA</a></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2025 Blackletter Systems. All rights reserved.</p>
        <p className="footer-disclaimer">
          Blackletter Systems provides software for compliance analysis. It does not provide legal advice. Results require professional review.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
