'use client';

import { useState } from 'react';
import { User, Mail, Phone, Calendar, MapPin, Briefcase, Award } from 'lucide-react';
import { useAuth } from '@/hooks';

export default function ProfilePage() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);

  // Mock user data - replace with actual user data from your auth system
  const [profile, setProfile] = useState({
    name: user?.name || 'Dr. Sarah Johnson',
    email: user?.email || 'sarah.johnson@hospital.com',
    phone: '+1 (555) 123-4567',
    role: user?.role || 'Cardiologist',
    specialization: 'Interventional Cardiology',
    licenseNumber: 'MD-123456',
    institution: 'Memorial Hospital',
    department: 'Cardiology Department',
    location: 'New York, NY',
    joinedDate: 'January 2024',
    bio: 'Board-certified cardiologist with 10+ years of experience in interventional cardiology and cardiac imaging.',
  });

  const handleSave = () => {
    console.log('Saving profile:', profile);
    setIsEditing(false);
    // TODO: Implement actual save functionality
    // await fetch('/api/user/profile', {
    //   method: 'PUT',
    //   body: JSON.stringify(profile)
    // });
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-5xl">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600">Manage your professional profile and credentials</p>
        </div>

        {/* Profile Card */}
        <div className="overflow-hidden rounded-lg bg-white shadow">
          {/* Cover Image */}
          <div className="h-32 bg-gradient-to-r from-blue-500 to-indigo-600"></div>

          {/* Profile Header */}
          <div className="relative px-6 pb-6">
            {/* Avatar */}
            <div className="absolute -top-16 left-6">
              <div className="flex h-32 w-32 items-center justify-center rounded-full border-4 border-white bg-gradient-to-br from-blue-400 to-indigo-500 text-4xl font-bold text-white shadow-lg">
                {profile.name.split(' ').map(n => n[0]).join('')}
              </div>
            </div>

            {/* Edit Button */}
            <div className="flex justify-end pt-4">
              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Edit Profile
                </button>
              ) : (
                <div className="flex gap-2">
                  <button
                    onClick={() => setIsEditing(false)}
                    className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Save Changes
                  </button>
                </div>
              )}
            </div>

            {/* Name and Role */}
            <div className="mt-16">
              {isEditing ? (
                <div className="space-y-3">
                  <input
                    type="text"
                    value={profile.name}
                    onChange={e => setProfile({ ...profile, name: e.target.value })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-2xl font-bold focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Full Name"
                  />
                  <input
                    type="text"
                    value={profile.role}
                    onChange={e => setProfile({ ...profile, role: e.target.value })}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-600 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Professional Role"
                  />
                </div>
              ) : (
                <>
                  <h2 className="text-2xl font-bold text-gray-900">{profile.name}</h2>
                  <p className="text-lg text-gray-600">{profile.role}</p>
                </>
              )}
            </div>

            {/* Bio */}
            <div className="mt-4">
              {isEditing ? (
                <textarea
                  value={profile.bio}
                  onChange={e => setProfile({ ...profile, bio: e.target.value })}
                  rows={3}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-gray-700 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Professional bio"
                />
              ) : (
                <p className="text-gray-700">{profile.bio}</p>
              )}
            </div>
          </div>

          {/* Profile Details */}
          <div className="border-t border-gray-200 px-6 py-6">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Contact Information</h3>
            <div className="grid gap-4 md:grid-cols-2">
              <ProfileField
                icon={<Mail className="h-5 w-5" />}
                label="Email"
                value={profile.email}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, email: value })}
                type="email"
              />
              <ProfileField
                icon={<Phone className="h-5 w-5" />}
                label="Phone"
                value={profile.phone}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, phone: value })}
                type="tel"
              />
              <ProfileField
                icon={<MapPin className="h-5 w-5" />}
                label="Location"
                value={profile.location}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, location: value })}
              />
              <ProfileField
                icon={<Calendar className="h-5 w-5" />}
                label="Member Since"
                value={profile.joinedDate}
                isEditing={false}
              />
            </div>
          </div>

          {/* Professional Details */}
          <div className="border-t border-gray-200 px-6 py-6">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">
              Professional Information
            </h3>
            <div className="grid gap-4 md:grid-cols-2">
              <ProfileField
                icon={<Briefcase className="h-5 w-5" />}
                label="Institution"
                value={profile.institution}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, institution: value })}
              />
              <ProfileField
                icon={<User className="h-5 w-5" />}
                label="Department"
                value={profile.department}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, department: value })}
              />
              <ProfileField
                icon={<Award className="h-5 w-5" />}
                label="Specialization"
                value={profile.specialization}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, specialization: value })}
              />
              <ProfileField
                icon={<Award className="h-5 w-5" />}
                label="License Number"
                value={profile.licenseNumber}
                isEditing={isEditing}
                onChange={value => setProfile({ ...profile, licenseNumber: value })}
              />
            </div>
          </div>

          {/* Statistics */}
          <div className="border-t border-gray-200 bg-gray-50 px-6 py-6">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Activity Summary</h3>
            <div className="grid gap-4 md:grid-cols-4">
              <StatCard label="Assessments" value="127" />
              <StatCard label="Reports Generated" value="89" />
              <StatCard label="Patients Analyzed" value="156" />
              <StatCard label="This Month" value="23" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper Components
function ProfileField({
  icon,
  label,
  value,
  isEditing,
  onChange,
  type = 'text',
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  isEditing: boolean;
  onChange?: (value: string) => void;
  type?: string;
}) {
  return (
    <div className="flex items-start gap-3">
      <div className="mt-1 text-gray-400">{icon}</div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-500">{label}</p>
        {isEditing && onChange ? (
          <input
            type={type}
            value={value}
            onChange={e => onChange(e.target.value)}
            className="mt-1 w-full rounded-md border border-gray-300 px-2 py-1 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        ) : (
          <p className="mt-1 text-gray-900">{value}</p>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-white p-4 shadow-sm">
      <p className="text-sm font-medium text-gray-500">{label}</p>
      <p className="mt-2 text-3xl font-bold text-blue-600">{value}</p>
    </div>
  );
}