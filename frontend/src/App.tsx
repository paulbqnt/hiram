import React from 'react';
import AppRouter from './Router';
import ErrorBoundary from './components/ErrorBoundary';
import {ThemeProvider} from "@/components/theme-provider.tsx";
import Layout from "@/components/Layout.tsx";

const App: React.FC = () => {
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <ErrorBoundary>
                <Layout>
                    <AppRouter />
                </Layout>
            </ErrorBoundary>
        </ThemeProvider>
    );
};

export default App;
