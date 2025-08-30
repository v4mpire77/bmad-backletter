import React from 'react';

const Navbar = () => {
  return (
    <nav id="navbar">
      <div className="nav-container">
        <div className="logo">Blackletter Systems</div>
        <ul className="nav-links">
          <li><a href="#how-it-works">How it works</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
        <button className="theme-toggle" onClick={() => {
          const body = document.body;
          const themeIcon = document.getElementById('theme-icon');

          if (body.classList.contains('dark-theme')) {
              body.classList.remove('dark-theme');
              if (themeIcon) themeIcon.textContent = '🌙 Dark';
          } else {
              body.classList.add('dark-theme');
              if (themeIcon) themeIcon.textContent = '☀️ Light';
          }
        }}>
          <span id="theme-icon">☀️ Light</span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
