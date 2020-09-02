import CreateContactDto from "../../dto/create-contact.dto";
import Contact from './contact.entity';
import { ContactsService } from './contacts.service';
export declare class ContactsController {
    private readonly contactsService;
    constructor(contactsService: ContactsService);
    create(createContactDto: CreateContactDto): Promise<Contact>;
    findAll(): Promise<{
        contactsList: Contact[];
    }>;
    find_by_id(id: string): Promise<{
        hasContact: boolean;
        firstName?: undefined;
        lastName?: undefined;
        phoneNumber?: undefined;
        isActive?: undefined;
    } | {
        firstName: any;
        lastName: any;
        phoneNumber: any;
        isActive: any;
        hasContact: boolean;
    }>;
    remove(id: string): Promise<{
        hasContact: boolean;
        firstName?: undefined;
        lastName?: undefined;
        phoneNumber?: undefined;
        isActive?: undefined;
    } | {
        firstName: any;
        lastName: any;
        phoneNumber: any;
        isActive: any;
        hasContact: boolean;
    }>;
}
