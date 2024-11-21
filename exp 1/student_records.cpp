#include <bits/stdc++.h>

using namespace std;

class Student
{
public:
    int adm_no;
    int marks;
    string branch;

    Student(int a, int m, string b)
    {
        this->adm_no = a;
        this->marks = m;
        this->branch = b;
    }
};

class node
{
public:
    Student data;
    node *next;
    node *prev;

    node(Student val) : data(val)
    {
        this->next = NULL;
        this->prev = NULL;
    }
};

void appendNode(node *&head, Student val)
{
    node *new_node = new node(val);
    if (head == NULL)
    {
        head = new_node;
        return;
    }
    node *temp = head;
    while (temp->next != NULL)
    {
        temp = temp->next;
    }
    temp->next = new_node;
    new_node->prev = temp;
}

void display(node *head)
{
    node *temp = head;
    while (temp != NULL)
    {
        cout << "Adm No: " << temp->data.adm_no << ", Marks: " << temp->data.marks << ", Branch: " << temp->data.branch << "\n";
        temp = temp->next;
    }
}

int main()
{
    node *head = NULL;
    int choice;

    while (true)
    {
        cout << "\nMenu:\n";
        cout << "1. Insert\n";
        cout << "2. View\n";
        cout << "3. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice)
        {
        case 1:
        {
            int adm_no, marks;
            string branch;
            cout << "Enter admission number: ";
            cin >> adm_no;
            cout << "Enter marks: ";
            cin >> marks;
            cout << "Enter branch: ";
            cin >> branch;
            appendNode(head, Student(adm_no, marks, branch));
            break;
        }

        case 2:
        {
            display(head);
            break;
        }

        case 3:
        {
            return 0;
        }

        default:
            cout << "invalid option" << endl;
            break;
        }
    }

    return 0;
}
