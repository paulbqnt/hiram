// src/pages/Portfolios.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';

const Portfolios: React.FC = () => {
    return (
        <div>
            <h1>Portfolios</h1>
            <Outlet />
        </div>
    );
};

export default Portfolios;