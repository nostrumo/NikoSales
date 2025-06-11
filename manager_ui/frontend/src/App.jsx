const { useState } = React;
import ChatPage from './ChatPage.jsx';
import ShopSettingsPage from './ShopSettingsPage.jsx';
import { ThemeProvider, useTheme } from './ThemeContext.jsx';

function Navigation({ current, onChange }) {
    const { toggleTheme } = useTheme();
    return (
        <nav className="navigation">
            <button className={current === 'chat' ? 'active' : ''} onClick={() => onChange('chat')}>Чат</button>
            <button className={current === 'settings' ? 'active' : ''} onClick={() => onChange('settings')}>Настройки</button>
            <button onClick={toggleTheme}>Сменить тему</button>
        </nav>
    );
}

export default function App() {
    const [page, setPage] = useState('chat');
    return (
        <ThemeProvider>
            <Navigation current={page} onChange={setPage} />
            {page === 'chat' ? <ChatPage /> : <ShopSettingsPage />}
        </ThemeProvider>
    );
}
