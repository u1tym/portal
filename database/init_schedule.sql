create database portal_schedule encoding 'utf8' owner puser;

-- スケジュール管理用テーブル作成

-- アクティビティカテゴリテーブル
CREATE TABLE IF NOT EXISTS activity_categories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name CHARACTER VARYING(255) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_activity_categories_user_id ON activity_categories(user_id);

-- スケジュールテーブル
CREATE TABLE IF NOT EXISTS schedules (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title CHARACTER VARYING(255) NOT NULL,
    is_all_day BOOLEAN NOT NULL DEFAULT FALSE,
    start_datetime TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL,
    duration INTEGER NOT NULL,
    activity_category_id INTEGER,
    schedule_type CHARACTER VARYING(50),
    location CHARACTER VARYING(255),
    details TEXT,
    is_todo_completed BOOLEAN NOT NULL DEFAULT FALSE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP(6) WITHOUT TIME ZONE NOT NULL,
    FOREIGN KEY (activity_category_id) REFERENCES activity_categories(id)
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_schedules_user_id ON schedules(user_id);
CREATE INDEX IF NOT EXISTS idx_schedules_start_datetime ON schedules(start_datetime);
CREATE INDEX IF NOT EXISTS idx_schedules_activity_category_id ON schedules(activity_category_id);
CREATE INDEX IF NOT EXISTS idx_schedules_is_deleted ON schedules(is_deleted);

-- サンプルデータ挿入（テスト用）
INSERT INTO activity_categories (user_id, name, is_deleted, created_at, updated_at) VALUES
(2, '仕事', FALSE, NOW(), NOW()),
(2, 'プライベート', FALSE, NOW(), NOW()),
(2, '健康', FALSE, NOW(), NOW());

INSERT INTO schedules (user_id, title, is_all_day, start_datetime, duration, activity_category_id, schedule_type, location, details, is_todo_completed, is_deleted, created_at, updated_at) VALUES
(2, '会議', FALSE, '2024-01-15 10:00:00', 60, 1, 'meeting', '会議室A', 'プロジェクトの進捗確認', FALSE, FALSE, NOW(), NOW()),
(2, '休日', TRUE, '2024-01-20 00:00:00', 1, 2, 'holiday', '', '家族との時間', FALSE, FALSE, NOW(), NOW()),
(2, 'ジム', FALSE, '2024-01-18 18:00:00', 90, 3, 'exercise', 'フィットネスジム', '筋力トレーニング', FALSE, FALSE, NOW(), NOW());