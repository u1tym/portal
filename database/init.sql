-- ユーザ管理用テーブル
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- セッション管理テーブル
CREATE TABLE sessions (
    user_id INTEGER NOT NULL,
    key_value VARCHAR(255) NOT NULL,
    session_string VARCHAR(255),
    last_access_time TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, key_value),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- コンテンツ管理テーブル
CREATE TABLE contents (
    user_id INTEGER NOT NULL,
    display_order INTEGER NOT NULL,
    content_title VARCHAR(255),
    redirect_url VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, display_order),
    UNIQUE (display_order),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Sample data
INSERT INTO users (username, password) VALUES
('admin', 'admin123'),
('user1', 'password123');

INSERT INTO contents (user_id, display_order, content_title, redirect_url) VALUES
(1, 0, 'Admin Panel', 'https://admin.example.com'),
(2, 1, 'User Panel', 'https://user.example.com');
