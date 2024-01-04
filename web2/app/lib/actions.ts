'use server';

import { signIn } from "@/auth";
import { sql } from "@vercel/postgres";
import { AuthError } from "next-auth";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

// This is temporary until @types/react-dom is updated
export type State = {
    errors?: {
      customerId?: string[];
      amount?: string[];
      status?: string[];
    };
    message?: string | null;
  };

// Define a schema that matches the shape of your form object.
// This schema will validate the formData before saving it to a database.
const FormSchema = z.object({
    id: z.string(),
    amount: z.coerce
        .number()
        .gt(0, { message: 'Please enter a number greater than $0.' }),
    status: z.enum(['pending', 'paid'], {
        invalid_type_error: 'Please select an invoice status.',
    }),
    date: z.string(),
});

// Omit ID and date since we don't have those fields (yet).
const CreateInvoice = FormSchema.omit({ id: true, date: true });
const UpdateInvoice = FormSchema.omit({ id: true, date: true });

const invoicesPath = '/dashboard/transactions';

export async function createInvoice(previousState: State, formData: FormData) {
    // Note: If you're working with forms that have many fields, you may want to consider using Object.fromEntries().
    // For example: const rawFormData = Object.fromEntries(formData.entries())
    // Validate fields with zod
    const validatedFields = CreateInvoice.safeParse({
        amount: formData.get('amount'),
        status: formData.get('status'),
    });

    // If form validation fails, return errors early. Otherwise, continue.
    if (!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Missing Fields. Failed to Create Invoice.',
        };
    }

    const { amount, status } = validatedFields.data;
    // It's usually good practice to store monetary values in cents in your database
    // to eliminate JavaScript floating-point errors and ensure greater accuracy.
    const amountInCents = amount * 100;
    // Create a new date with the format "YYYY-MM-DD" for the invoice's creation date
    const date = new Date().toISOString().split('T')[0];

    try {
        await sql`
            INSERT INTO invoices (customer_id, amount, status, date)
            VALUES (12345, ${amountInCents}, ${status}, ${date})
        `;
    } catch(error) {
        return { message: "Database error: failed to create invoice." };
    }

    // Since you're updating the data displayed in the invoices route, clear the Next.js client-side router cache
    // to trigger a new request to the server, and redirect to that route.
    revalidatePath(invoicesPath);
    // Note: redirect should be called outside of the try/catch block.
    // This is because redirect works by throwing an error, which would be
    // caught by the catch block.
    redirect(invoicesPath);
}

export async function updateInvoice(id: string, previousState: State, formData: FormData) {
    const validatedFields = UpdateInvoice.safeParse({
        customerId: formData.get('customerId'),
        amount: formData.get('amount'),
        status: formData.get('status'),
    });
    if (!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Missing Fields. Failed to Update Invoice.',
        };
    }
    const { amount, status } = validatedFields.data;
    const amountInCents = amount * 100;

    try {
        await sql`
            UPDATE invoices
            SET amount = ${amountInCents}, status = ${status}
            WHERE id = ${id}
        `;
    } catch(error) {
        return { message: "Database error: failed to update invoice." };
    }

    revalidatePath(invoicesPath);
    redirect(invoicesPath);
}

export async function deleteInvoice(id: string) {
    try {
        await sql`
            DELETE FROM invoices WHERE id = ${id}
        `;
        revalidatePath(invoicesPath);
    } catch(error) {
        return { message: "Database error: failed to delete invoice." };
    }
}

export async function authenticate(
    prevState: string | undefined,
    formData: FormData) {
    try {
        await signIn('credentials', formData);
    } catch (error) {
        if (error instanceof AuthError) {
            switch (error.type) {
            case 'CredentialsSignin':
                return 'Invalid credentials.';
            default:
                return 'Something went wrong.';
            }
        }
        throw error;
    }
  }
