// src/Router.tsx
import React, { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const HomePage = lazy(() => import('./pages/Home'));
const LoginPage = lazy(() => import('./pages/Login.tsx'))
const DashboardPage = lazy(() => import('./pages/Dashboard.tsx'))
const PricerPage = lazy(() => import('./pages/Pricer.tsx'))
const PortfoliosPage = lazy(() => import('./pages/Portfolios.tsx'))
const ResourcesPage = lazy(() => import('./pages/Resources.tsx'))
const SignupPage = lazy(() => import('./pages/Signup.tsx'))
const NotFoundPage = lazy(() => import('./pages/NotFound'));


const AppRouter: React.FC = () => {
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/pricer" element={<PricerPage />} />
                    <Route path="/portfolios" element={<PortfoliosPage />} />
                    <Route path="/resources" element={<ResourcesPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/signup" element={<SignupPage />} />
                    <Route path="*" element={<NotFoundPage />} />
                </Routes>
            </Suspense>
        </Router>
    );
};

export default AppRouter;