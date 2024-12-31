import React, {lazy} from 'react';
import { Button } from "@/components/ui/button";


const Navbar = () => {
    const navItems = [
        { label: 'Home', href: '/' },
        { label: 'Dashboard', href: '/dashboard' },
        { label: 'Pricer', href: '/pricer' },
        { label: 'Portfolios', href: '/portfolios' },
        { label: 'Resources', href: '/resources' },
    ];

    return (
        <nav className="w-full bg-background  border-gray-100 fixed top-0 z-50 border-2 border-red-500 p-4">
            <div className="max-w-7xl mx-auto px-4 ">
                <div className="flex items-center h-16 justify-between">
                    {/* Logo */}
                    <div className="flex-shrink-0 ">
                        <span className="text-xl font-bold">Logo</span>
                    </div>

                    {/* Navigation Items */}
                    <div className="flex space-x-8 ">
                        {navItems.map((item) => (
                            <a
                                key={item.label}
                                href={item.href}
                                className="text-gray-200 hover:text-gray-400 px-3 py-2 rounded-md text-sm font-medium border-2 border-red-500 p-4"
                            >
                                {item.label}
                            </a>
                        ))}
                    </div>

                    {/* Optional: Add a Call-to-Action button */}
                    <div>
                        <Button>Login</Button>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
