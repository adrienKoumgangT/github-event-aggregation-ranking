import React, { createContext, useContext, useState, useCallback, type ReactNode } from 'react';

interface AppState {
    refreshInterval: number;
    autoRefresh: boolean;
    darkMode: boolean;
    clusterUrl: string;
}

interface AppContextType extends AppState {
    setRefreshInterval: (interval: number) => void;
    toggleAutoRefresh: () => void;
    toggleDarkMode: () => void;
    setClusterUrl: (url: string) => void;
    triggerRefresh: () => void;
    refreshKey: number;
}

const defaultState: AppState = {
    refreshInterval: 5000,
    autoRefresh: true,
    darkMode: false,
    clusterUrl: 'http://localhost:5000/api/v1',
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useAppContext must be used within AppProvider');
    }
    return context;
};

interface AppProviderProps {
    children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
    const [state, setState] = useState<AppState>(() => {
        const saved = localStorage.getItem('appSettings');
        return saved ? { ...defaultState, ...JSON.parse(saved) } : defaultState;
    });
    const [refreshKey, setRefreshKey] = useState(0);

    const saveState = (newState: AppState) => {
        localStorage.setItem('appSettings', JSON.stringify(newState));
        setState(newState);
    };

    const setRefreshInterval = useCallback((interval: number) => {
        saveState({ ...state, refreshInterval: interval });
    }, [state]);

    const toggleAutoRefresh = useCallback(() => {
        saveState({ ...state, autoRefresh: !state.autoRefresh });
    }, [state]);

    const toggleDarkMode = useCallback(() => {
        saveState({ ...state, darkMode: !state.darkMode });
    }, [state]);

    const setClusterUrl = useCallback((url: string) => {
        saveState({ ...state, clusterUrl: url });
    }, [state]);

    const triggerRefresh = useCallback(() => {
        setRefreshKey((prev) => prev + 1);
    }, []);

    const value: AppContextType = {
        ...state,
        setRefreshInterval,
        toggleAutoRefresh,
        toggleDarkMode,
        setClusterUrl,
        triggerRefresh,
        refreshKey,
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

export default AppContext;
