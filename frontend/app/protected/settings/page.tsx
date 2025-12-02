'use client';

import { useState } from 'react';
import {
  Bell,
  Lock,
  User,
  Globe,
  Shield,
  Moon,
  Mail,
  Smartphone,
  Database,
  AlertTriangle,
} from 'lucide-react';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general');

  const tabs = [
    { id: 'general', label: 'General', icon: <User className="h-4 w-4" /> },
    { id: 'security', label: 'Security', icon: <Lock className="h-4 w-4" /> },
    { id: 'notifications', label: 'Notifications', icon: <Bell className="h-4 w-4" /> },
    { id: 'privacy', label: 'Privacy', icon: <Shield className="h-4 w-4" /> },
    { id: 'advanced', label: 'Advanced', icon: <Database className="h-4 w-4" /> },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600">Manage your account preferences and security</p>
        </div>

        <div className="flex gap-6">
          {/* Sidebar */}
          <div className="w-64 flex-shrink-0">
            <nav className="space-y-1 rounded-lg bg-white p-2 shadow">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex w-full items-center gap-3 rounded-md px-3 py-2 text-left text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Content */}
          <div className="flex-1">
            <div className="rounded-lg bg-white p-6 shadow">
              {activeTab === 'general' && <GeneralSettings />}
              {activeTab === 'security' && <SecuritySettings />}
              {activeTab === 'notifications' && <NotificationSettings />}
              {activeTab === 'privacy' && <PrivacySettings />}
              {activeTab === 'advanced' && <AdvancedSettings />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// General Settings Tab
function GeneralSettings() {
  const [settings, setSettings] = useState({
    language: 'en',
    timezone: 'America/New_York',
    dateFormat: 'MM/DD/YYYY',
    theme: 'light',
  });

  const handleSave = () => {
    console.log('Saving settings:', settings);
    // TODO: API call to save settings
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">General Settings</h2>
        <p className="text-sm text-gray-600">Customize your experience</p>
      </div>

      {/* Language */}
      <SettingItem
        icon={<Globe className="h-5 w-5" />}
        label="Language"
        description="Select your preferred language"
      >
        <select
          value={settings.language}
          onChange={e => setSettings({ ...settings, language: e.target.value })}
          className="rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="en">English</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="de">German</option>
        </select>
      </SettingItem>

      {/* Timezone */}
      <SettingItem
        icon={<Globe className="h-5 w-5" />}
        label="Timezone"
        description="Set your local timezone"
      >
        <select
          value={settings.timezone}
          onChange={e => setSettings({ ...settings, timezone: e.target.value })}
          className="rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="America/New_York">Eastern Time (ET)</option>
          <option value="America/Chicago">Central Time (CT)</option>
          <option value="America/Denver">Mountain Time (MT)</option>
          <option value="America/Los_Angeles">Pacific Time (PT)</option>
        </select>
      </SettingItem>

      {/* Theme */}
      <SettingItem
        icon={<Moon className="h-5 w-5" />}
        label="Appearance"
        description="Choose light or dark mode"
      >
        <div className="flex gap-2">
          <button
            onClick={() => setSettings({ ...settings, theme: 'light' })}
            className={`rounded-md border px-4 py-2 transition-colors ${
              settings.theme === 'light'
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Light
          </button>
          <button
            onClick={() => setSettings({ ...settings, theme: 'dark' })}
            className={`rounded-md border px-4 py-2 transition-colors ${
              settings.theme === 'dark'
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Dark
          </button>
        </div>
      </SettingItem>

      <div className="pt-4">
        <button
          onClick={handleSave}
          className="rounded-md bg-blue-600 px-4 py-2 text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Save Changes
        </button>
      </div>
    </div>
  );
}

// Security Settings Tab
function SecuritySettings() {
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Security Settings</h2>
        <p className="text-sm text-gray-600">Manage your account security</p>
      </div>

      {/* Change Password */}
      <SettingItem
        icon={<Lock className="h-5 w-5" />}
        label="Change Password"
        description="Update your password regularly for security"
      >
        <button
          onClick={() => setShowPasswordModal(true)}
          className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Change Password
        </button>
      </SettingItem>

      {/* Two-Factor Authentication */}
      <SettingItem
        icon={<Smartphone className="h-5 w-5" />}
        label="Two-Factor Authentication"
        description="Add an extra layer of security to your account"
      >
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-600">Not enabled</span>
          <button className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
            Enable 2FA
          </button>
        </div>
      </SettingItem>

      {/* Active Sessions */}
      <SettingItem
        icon={<User className="h-5 w-5" />}
        label="Active Sessions"
        description="Manage devices where you're logged in"
      >
        <button className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
          View Sessions
        </button>
      </SettingItem>

      {/* Login History */}
      <SettingItem
        icon={<Shield className="h-5 w-5" />}
        label="Login History"
        description="Review recent login activity"
      >
        <button className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
          View History
        </button>
      </SettingItem>
    </div>
  );
}

// Notification Settings Tab
function NotificationSettings() {
  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    pushNotifications: false,
    assessmentComplete: true,
    reportReady: true,
    systemUpdates: false,
    weeklyDigest: true,
  });

  const toggle = (key: keyof typeof notifications) => {
    setNotifications({ ...notifications, [key]: !notifications[key] });
  };

  const handleSave = () => {
    console.log('Saving notifications:', notifications);
    // TODO: API call to save notification preferences
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Notification Settings</h2>
        <p className="text-sm text-gray-600">Choose how you want to be notified</p>
      </div>

      {/* Email Notifications */}
      <SettingToggle
        icon={<Mail className="h-5 w-5" />}
        label="Email Notifications"
        description="Receive notifications via email"
        enabled={notifications.emailNotifications}
        onToggle={() => toggle('emailNotifications')}
      />

      {/* Push Notifications */}
      <SettingToggle
        icon={<Bell className="h-5 w-5" />}
        label="Push Notifications"
        description="Receive push notifications in your browser"
        enabled={notifications.pushNotifications}
        onToggle={() => toggle('pushNotifications')}
      />

      <div className="border-t pt-6">
        <h3 className="mb-4 text-lg font-medium text-gray-900">Notification Types</h3>

        <div className="space-y-4">
          <SettingToggle
            label="Assessment Complete"
            description="Notify when an assessment is completed"
            enabled={notifications.assessmentComplete}
            onToggle={() => toggle('assessmentComplete')}
          />

          <SettingToggle
            label="Report Ready"
            description="Notify when a report is generated"
            enabled={notifications.reportReady}
            onToggle={() => toggle('reportReady')}
          />

          <SettingToggle
            label="System Updates"
            description="Notify about system maintenance and updates"
            enabled={notifications.systemUpdates}
            onToggle={() => toggle('systemUpdates')}
          />

          <SettingToggle
            label="Weekly Digest"
            description="Receive a weekly summary of your activity"
            enabled={notifications.weeklyDigest}
            onToggle={() => toggle('weeklyDigest')}
          />
        </div>
      </div>

      <div className="pt-4">
        <button
          onClick={handleSave}
          className="rounded-md bg-blue-600 px-4 py-2 text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Save Preferences
        </button>
      </div>
    </div>
  );
}

// Privacy Settings Tab
function PrivacySettings() {
  const [dataRetention, setDataRetention] = useState('forever');

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Privacy Settings</h2>
        <p className="text-sm text-gray-600">Control your data and privacy</p>
      </div>

      <SettingItem
        icon={<Database className="h-5 w-5" />}
        label="Data Export"
        description="Download all your data"
      >
        <button className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
          Request Export
        </button>
      </SettingItem>

      <SettingItem
        icon={<Shield className="h-5 w-5" />}
        label="Data Retention"
        description="Manage how long we keep your data"
      >
        <select
          value={dataRetention}
          onChange={e => setDataRetention(e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="forever">Keep forever</option>
          <option value="1year">1 year</option>
          <option value="6months">6 months</option>
          <option value="3months">3 months</option>
        </select>
      </SettingItem>
    </div>
  );
}

// Advanced Settings Tab
function AdvancedSettings() {
  const handleClearCache = () => {
    console.log('Clearing cache...');
    // TODO: Implement cache clearing
  };

  const handleDeleteAccount = () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      console.log('Deleting account...');
      // TODO: Implement account deletion
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Advanced Settings</h2>
        <p className="text-sm text-gray-600">Advanced options for power users</p>
      </div>

      <div className="rounded-lg border-2 border-red-200 bg-red-50 p-4">
        <div className="flex gap-3">
          <AlertTriangle className="h-5 w-5 flex-shrink-0 text-red-600" />
          <div>
            <h3 className="font-semibold text-red-900">Danger Zone</h3>
            <p className="mt-1 text-sm text-red-700">
              These actions are permanent and cannot be undone.
            </p>
          </div>
        </div>
      </div>

      <SettingItem
        icon={<Database className="h-5 w-5" />}
        label="Clear Cache"
        description="Clear all cached data"
      >
        <button
          onClick={handleClearCache}
          className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Clear Cache
        </button>
      </SettingItem>

      <SettingItem
        icon={<AlertTriangle className="h-5 w-5 text-red-600" />}
        label="Delete Account"
        description="Permanently delete your account and all data"
      >
        <button
          onClick={handleDeleteAccount}
          className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Delete Account
        </button>
      </SettingItem>
    </div>
  );
}

// Helper Components
function SettingItem({
  icon,
  label,
  description,
  children,
}: {
  icon?: React.ReactNode;
  label: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-start justify-between border-b border-gray-200 pb-6">
      <div className="flex gap-3">
        {icon && <div className="text-gray-400">{icon}</div>}
        <div>
          <h3 className="font-medium text-gray-900">{label}</h3>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
      </div>
      <div className="flex-shrink-0">{children}</div>
    </div>
  );
}

function SettingToggle({
  icon,
  label,
  description,
  enabled,
  onToggle,
}: {
  icon?: React.ReactNode;
  label: string;
  description: string;
  enabled: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="flex items-start justify-between border-b border-gray-200 pb-4">
      <div className="flex gap-3">
        {icon && <div className="text-gray-400">{icon}</div>}
        <div>
          <h3 className="font-medium text-gray-900">{label}</h3>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
      </div>
      <button
        onClick={onToggle}
        className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
          enabled ? 'bg-blue-600' : 'bg-gray-200'
        }`}
        role="switch"
        aria-checked={enabled}
      >
        <span
          className={`inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
            enabled ? 'translate-x-5' : 'translate-x-0'
          }`}
        />
      </button>
    </div>
  );
}