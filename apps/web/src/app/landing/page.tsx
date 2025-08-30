"use client";

import React, { useEffect } from 'react';
import Navbar from '@/components/landing/Navbar';
import Hero from '@/components/landing/Hero';
import SocialProof from '@/components/landing/SocialProof';
import WhyBlackletter from '@/components/landing/WhyBlackletter';
import HowItWorks from '@/components/landing/HowItWorks';
import GdprChecks from '@/components/landing/GdprChecks';
import Faq from '@/components/landing/Faq';
import Footer from '@/components/landing/Footer';
import '@/styles/landing.css';

const LandingPage = () => {
  useEffect(() => {
    // Navbar scroll effect
    const onScroll = () => {
        const navbar = document.getElementById('navbar');
        if (navbar && window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else if (navbar) {
            navbar.classList.remove('scrolled');
        }
    };
    window.addEventListener('scroll', onScroll);
    onScroll(); // run on initial render

    // Smooth scrolling for navigation links
    const smoothScroll = (e: MouseEvent) => {
        e.preventDefault();
        const targetId = (e.currentTarget as HTMLAnchorElement).getAttribute('href');
        if (targetId) {
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    };
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', smoothScroll as EventListener);
    });

    // Initialize animations on load
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((el, index) => {
        setTimeout(() => {
            (el as HTMLElement).style.opacity = '1';
            (el as HTMLElement).style.transform = 'translateY(0)';
        }, index * 100);
    });

    return () => {
        window.removeEventListener('scroll', onScroll);
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.removeEventListener('click', smoothScroll as EventListener);
        });
    };
  }, []);

  return (
    <>
      <div className="bg-elements">
        <div className="floating-gradient gradient-1"></div>
        <div className="floating-gradient gradient-2"></div>
        <div className="floating-gradient gradient-3"></div>
      </div>
      <Navbar />
      <div className="container">
        <Hero />
        <SocialProof />
        <WhyBlackletter />
        <HowItWorks />
        <GdprChecks />
        <Faq />
      </div>
      <Footer />
    </>
  );
};

export default LandingPage;
