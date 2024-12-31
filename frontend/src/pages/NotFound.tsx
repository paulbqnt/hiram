// src/pages/Home.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';

const NotFound: React.FC = () => {
    return (
        <div>
            <h1 className="scroll-m-20 border-b pb-2 text-6xl font-semibold tracking-tight first:mt-0">404</h1>
            <h2 className="scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight first:mt-0">Page not found</h2>
            <Outlet/>
        </div>
    );
};

export default NotFound;