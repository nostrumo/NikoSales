const { useState, useEffect } = React;

const topics = [
    { id: 'pricing', label: 'Цены' },
    { id: 'delivery', label: 'Доставка' },
    { id: 'returns', label: 'Возвраты' },
    { id: 'other', label: 'Прочее' },
];

export default function ShopSettingsPage() {
    const [form, setForm] = useState({
        name: '',
        data_content: '',
        shipping_info: '',
        location_info: '',
        ai_topics: [],
        manager_topics: [],
    });
    const shopId = 1; // заглушка

    useEffect(() => {
        fetch(`/shops/${shopId}`)
            .then(r => r.ok ? r.json() : null)
            .then(data => {
                if (data) {
                    setForm({
                        ...form,
                        ...data,
                        ai_topics: data.ai_topics ? data.ai_topics.split(',') : [],
                        manager_topics: data.manager_topics ? data.manager_topics.split(',') : [],
                    });
                }
            });
    }, []);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const toggleTopic = (listName, id) => {
        setForm(prev => {
            const set = new Set(prev[listName]);
            if (set.has(id)) set.delete(id); else set.add(id);
            return { ...prev, [listName]: Array.from(set) };
        });
    };

    const save = () => {
        const payload = {
            ...form,
            ai_topics: form.ai_topics.join(','),
            manager_topics: form.manager_topics.join(','),
        };
        fetch(`/shops/${shopId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
    };

    return (
        <form className="settings-form" onSubmit={e => { e.preventDefault(); save(); }}>
            <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="Название магазина"
            />
            <textarea
                name="data_content"
                value={form.data_content}
                onChange={handleChange}
                placeholder="Описание магазина"
            />
            <textarea
                name="shipping_info"
                value={form.shipping_info}
                onChange={handleChange}
                placeholder="Информация о доставке"
            />
            <textarea
                name="location_info"
                value={form.location_info}
                onChange={handleChange}
                placeholder="Месторасположение"
            />
            <div>
                <p>На что отвечает ИИ агент:</p>
                {topics.map(t => (
                    <label key={t.id}>
                        <input
                            type="checkbox"
                            checked={form.ai_topics.includes(t.id)}
                            onChange={() => toggleTopic('ai_topics', t.id)}
                        />
                        {t.label}
                    </label>
                ))}
            </div>
            <div>
                <p>На что отвечает менеджер:</p>
                {topics.map(t => (
                    <label key={t.id}>
                        <input
                            type="checkbox"
                            checked={form.manager_topics.includes(t.id)}
                            onChange={() => toggleTopic('manager_topics', t.id)}
                        />
                        {t.label}
                    </label>
                ))}
            </div>
            <button type="submit">Сохранить</button>
        </form>
    );
}
