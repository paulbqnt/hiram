import React from 'react';
import AppRouter from './Router';
import ErrorBoundary from './components/ErrorBoundary';
import {ThemeProvider} from "@/components/theme-provider.tsx";

const App: React.FC = () => {
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <ErrorBoundary>
                <AppRouter />
            </ErrorBoundary>
        </ThemeProvider>
    );
};

export default App;
