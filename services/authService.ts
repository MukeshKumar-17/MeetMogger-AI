import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import User, { IUser } from '../models/User';
import connectDB from '../lib/mongodb';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';

export interface AuthResponse {
  success: boolean;
  message: string;
  user?: {
    id: string;
    email: string;
    name: string;
  };
  token?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  name: string;
}

// Register a new user
export const registerUser = async (credentials: RegisterCredentials): Promise<AuthResponse> => {
  try {
    await connectDB();

    // Check if user already exists
    const existingUser = await User.findOne({ email: credentials.email });
    if (existingUser) {
      return {
        success: false,
        message: 'User with this email already exists',
      };
    }

    // Hash password
    const saltRounds = 12;
    const hashedPassword = await bcrypt.hash(credentials.password, saltRounds);

    // Create new user
    const user = new User({
      email: credentials.email,
      password: hashedPassword,
      name: credentials.name,
    });

    await user.save();

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, email: user.email },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    return {
      success: true,
      message: 'User registered successfully',
      user: {
        id: user._id.toString(),
        email: user.email,
        name: user.name,
      },
      token,
    };
  } catch (error) {
    console.error('Registration error:', error);
    return {
      success: false,
      message: 'Registration failed. Please try again.',
    };
  }
};

// Login user
export const loginUser = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    await connectDB();

    // Find user by email
    const user = await User.findOne({ email: credentials.email });
    if (!user) {
      return {
        success: false,
        message: 'Invalid email or password',
      };
    }

    // Check password
    const isPasswordValid = await bcrypt.compare(credentials.password, user.password);
    if (!isPasswordValid) {
      return {
        success: false,
        message: 'Invalid email or password',
      };
    }

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, email: user.email },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    return {
      success: true,
      message: 'Login successful',
      user: {
        id: user._id.toString(),
        email: user.email,
        name: user.name,
      },
      token,
    };
  } catch (error) {
    console.error('Login error:', error);
    return {
      success: false,
      message: 'Login failed. Please try again.',
    };
  }
};

// Verify JWT token
export const verifyToken = (token: string): { userId: string; email: string } | null => {
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as { userId: string; email: string };
    return decoded;
  } catch (error) {
    return null;
  }
};

// Get user by ID
export const getUserById = async (userId: string): Promise<IUser | null> => {
  try {
    await connectDB();
    const user = await User.findById(userId).select('-password');
    return user;
  } catch (error) {
    console.error('Get user error:', error);
    return null;
  }
};
