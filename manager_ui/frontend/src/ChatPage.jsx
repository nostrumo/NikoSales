/* Компонент страницы чата менеджера с пользователями. */
const { useState, useEffect, useRef } = React;

export default function ChatPage() {
    const [users, setUsers] = useState([]);
    const [currentUser, setCurrentUser] = useState(null);
    const [messages, setMessages] = useState([]);
    const [text, setText] = useState('');
    const wsRef = useRef(null);
    const bottomRef = useRef(null);

    useEffect(() => {
        // Загрузка списка пользователей магазина (заглушка)
        setUsers([{ id: 1, name: 'User 1' }, { id: 2, name: 'User 2' }]);
    }, []);

    useEffect(() => {
        if (!currentUser) return;

        fetch(`/messages/${currentUser.id}`)
            .then(r => r.ok ? r.json() : [])
            .then(setMessages);

        const ws = new WebSocket(`ws://${location.host}/ws/${currentUser.id}`);
        ws.onmessage = (e) => {
            setMessages(prev => [...prev, { role: 'user', content: e.data }]);
        };
        wsRef.current = ws;
        return () => ws.close();
    }, [currentUser]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const send = () => {
        if (wsRef.current && text.trim()) {
            wsRef.current.send(text);
            setMessages(prev => [...prev, { role: 'manager', content: text }]);
            setText('');
        }
    };

    return (
        <div className="chat-page">
            <aside className="user-list">
                {users.map(u => (
                    <button
                        key={u.id}
                        onClick={() => setCurrentUser(u)}
                        className={currentUser?.id === u.id ? 'active' : ''}
                    >
                        {u.name}
                    </button>
                ))}
            </aside>
            <section className="chat-window">
                <div className="messages">
                    {messages.map((m, i) => (
                        <div key={i} className={`message ${m.role}`}>{m.content}</div>
                    ))}
                    <div ref={bottomRef}></div>
                </div>
                {currentUser && (
                    <div className="input-area">
                        <input
                            value={text}
                            onChange={e => setText(e.target.value)}
                            placeholder="Введите сообщение"
                        />
                        <button onClick={send}>Отправить</button>
                    </div>
                )}
            </section>
        </div>
    );
}
