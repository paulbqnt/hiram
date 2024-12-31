// src/pages/Signup.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';

const Signup: React.FC = () => {
    return (
        <div>
            <h1>Signup</h1>
            <Outlet />
        </div>
    );
};

export default Signup;