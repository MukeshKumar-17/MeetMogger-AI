import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import mongoose from 'mongoose';

// MongoDB connection
const connectDB = async () => {
  try {
    const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/meetmogger-ai';
    await mongoose.connect(MONGODB_URI);
    console.log('✅ MongoDB connected successfully');
  } catch (error) {
    console.error('❌ MongoDB connection error:', error);
    throw error;
  }
};

// User Schema
const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters'],
  },
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true,
  },
}, {
  timestamps: true,
});

const User = mongoose.models.User || mongoose.model('User', userSchema);

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';

// Register a new user
export const registerUser = async (credentials) => {
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
export const loginUser = async (credentials) => {
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
