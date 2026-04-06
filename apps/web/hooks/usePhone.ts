import { useEffect, useState } from "react";

interface UserProfile {
  id: string;
  email: string;
  name?: string;
  phone?: string;
  country_code?: string;
  role: string;
}

const LOCAL_STORAGE_KEY = "nevumo_phone";
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function usePhone() {
  const [phone, setPhoneState] = useState<string>("");
  const [loading, setLoading] = useState(true);

  // Save phone to localStorage
  const savePhoneToStorage = (phoneValue: string) => {
    if (typeof window !== "undefined") {
      if (phoneValue) {
        localStorage.setItem(LOCAL_STORAGE_KEY, phoneValue);
      } else {
        localStorage.removeItem(LOCAL_STORAGE_KEY);
      }
    }
  };

  // Get current user and token
  const getCurrentAuth = () => {
    if (typeof window === "undefined") return { user: null, token: null };
    
    try {
      const token = localStorage.getItem("nevumo_auth_token");
      const userRaw = localStorage.getItem("nevumo_auth_user");
      const user = userRaw ? JSON.parse(userRaw) : null;
      return { user, token };
    } catch {
      return { user: null, token: null };
    }
  };

  // Fetch user profile from API
  const fetchUserProfile = async (token: string): Promise<UserProfile | null> => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/user/profile`, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        return null;
      }

      const result = await response.json();
      return result.success ? result.data : null;
    } catch {
      return null;
    }
  };

  // Update user profile via API (fire and forget)
  const updateProfile = async (token: string, phoneValue: string) => {
    try {
      await fetch(`${API_BASE}/api/v1/user/profile`, {
        method: "PATCH",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ phone: phoneValue }),
      });
    } catch {
      // Silent fail - background sync should never throw to UI
    }
  };

  // Initialize on mount
  useEffect(() => {
    const initializePhone = async () => {
      setLoading(true);
      
      const { user, token } = getCurrentAuth();
      
      if (user && token) {
        // User is logged in - fetch profile
        try {
          const profile = await fetchUserProfile(token);
          
          if (profile) {
            // Use profile phone if exists
            if (profile.phone) {
              setPhoneState(profile.phone);
            } else {
              // Profile phone is null, check localStorage for sync
              const localPhone = localStorage.getItem(LOCAL_STORAGE_KEY);
              if (localPhone) {
                setPhoneState(localPhone);
                // Silent background sync
                updateProfile(token, localPhone);
              } else {
                setPhoneState("");
              }
            }
          } else {
            // Fallback to localStorage if API fails
            const localPhone = localStorage.getItem(LOCAL_STORAGE_KEY) || "";
            setPhoneState(localPhone);
          }
        } catch {
          // Fallback to localStorage if everything fails
          const localPhone = localStorage.getItem(LOCAL_STORAGE_KEY) || "";
          setPhoneState(localPhone);
        }
      } else {
        // User not logged in - read from localStorage only
        const localPhone = localStorage.getItem(LOCAL_STORAGE_KEY) || "";
        setPhoneState(localPhone);
      }
      
      setLoading(false);
    };

    initializePhone();
  }, []);

  // Save phone function
  const savePhone = (phoneValue: string) => {
    // Always save to localStorage immediately
    setPhoneState(phoneValue);
    savePhoneToStorage(phoneValue);
    
    // If logged in, sync to profile in background
    const { token } = getCurrentAuth();
    if (token) {
      updateProfile(token, phoneValue);
    }
  };

  // Clear phone function
  const clearPhone = () => {
    setPhoneState("");
    savePhoneToStorage("");
    
    // If logged in, clear profile phone in background
    const { token } = getCurrentAuth();
    if (token) {
      updateProfile(token, "");
    }
  };

  return {
    phone,
    savePhone,
    clearPhone,
    loading,
  };
}
